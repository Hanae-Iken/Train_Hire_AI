import html
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from utils.GemeniAiModel import GenerativeModelClient
from django.conf import settings
import PyPDF2
import os
import requests
import json
from common.models import CV, Utilisateur, AbstractBaseUser, BaseUserManager, CustomUserManager
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import logging
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
import assemblyai as aai
from textblob import TextBlob
import logging
from dotenv import load_dotenv
load_dotenv(dotenv_path= "django4/.env")
DG_API_KEY = os.getenv('DG_API_KEY')
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
import tempfile

def extract_text_from_pdf(pdf_file_path: str) -> str:
    """Extract text from a PDF file."""
    full_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_file_path)  # Join the path with MEDIA_ROOT
    with open(full_pdf_path, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            if content:  # Ensure content is not None
                pdf_text.append(content)

        return "\n".join(pdf_text)


def generate_interview_questions(resume_text: str, domain: str, title: str, description: str, 
                                 skills: str, num_questions: int, language: str, level: str, is_general: bool) -> dict:
    """
    Generate interview questions based on the provided data.
    If `is_general` is True, skips domain, title, description, and skills.
    """
    if is_general:
        user_input = (f"Generate {num_questions} general interview questions.Include a mix of questions: some based on the following resume text: {resume_text}, "
                      f"and others unrelated to the resume ,"
                      f"Include questions about soft skills,"
                      f"Language of interview: {language}, difficulty level : {level}. Give the results in JSON format.")
    else:
        user_input = (f"Generate {num_questions} interview questions.Include a mix of questions: some based on the following resume text: {resume_text}, "
                      f"job title: {title}, domain: {domain}, job description: {description}, "
                      f"required skills: {skills}, "
                      f"and others unrelated to the resume or job,"
                      f"Include questions about soft skills,"
                      f"Language of interview: {language}, difficulty level:{level}. Give the results in JSON format.")

    model_client = GenerativeModelClient()
    response_text = model_client.get_response(user_input)
    
    # Unescape HTML and extract JSON
    clean_response = html.unescape(response_text).strip()
    if clean_response.startswith("```json"):
        clean_response = clean_response[7:-3].strip() 

    try:
        return json.loads(clean_response)
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response as JSON."}


def handle_resume_selection_or_upload(request, user):
    """Helper function to handle resume selection or upload."""
    selected_resume_id = request.POST.get('selected_resume')
    uploaded_resume = request.FILES.get('uploaded_resume')
    pdf_path = None
    
    if not selected_resume_id and not uploaded_resume:
        return None, 'Please select or upload a resume to begin the interview.', 400

    if uploaded_resume:
        try:
            # Handle resume upload
            new_resume = CV(utilisateur=user, resume=uploaded_resume)
            new_resume.save()

            pdf_path = new_resume.resume.path
        except Exception as e:
            return None, f'Error uploading resume: {str(e)}', 500
    elif selected_resume_id:
        # Handle resume selection
        try:
            selected_resume = CV.objects.get(id=selected_resume_id, utilisateur=user)
            pdf_path = selected_resume.resume.path
        except CV.DoesNotExist:
            return None, 'Selected resume not found or does not belong to the user.', 404

    return pdf_path, None, None


logger = logging.getLogger(__name__)

@login_required(login_url='/api/signin/')  # Redirect to a custom login page
@csrf_exempt
def gen_personalized_interview(request):
    if request.method == 'GET':
        # Redirect the GET request to the login page if the user is not authenticated
        if not request.user.is_authenticated:
            return redirect('/api/signin/')  # Customize your login URL here
        
        return JsonResponse({'error': 'Method "GET" not allowed. Only POST requests are accepted.'}, status=405)

    if request.method == 'POST':
        # User is authenticated, continue with the POST logic
        user = request.user
        logger.info("User: %s", user)

        # Ensure the user is of the correct type (if needed)
        if not isinstance(user, Utilisateur):
            return JsonResponse({'error': 'Unauthorized user type.'}, status=403)

        # Continue with the logic for handling POST requests...
        pdf_path, error_message, status_code = handle_resume_selection_or_upload(request, user)

        if error_message:
            return JsonResponse({'error': error_message}, status=status_code)

        # Extract form data
        domain = request.POST.get('domain')
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')
        num_questions = int(request.POST.get('num_questions'))
        language = request.POST.get('language')
        level = request.POST.get('level')

        # Process the resume to extract text
        resume_text = extract_text_from_pdf(pdf_path)

        # Generate questions
        response_text = generate_interview_questions(
            resume_text, domain, title, description, skills, num_questions, language, level, is_general=False
        )

        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required
@csrf_exempt
def gen_general_interview(request):
    if request.method == 'POST':
        # Get the user (ensure the user is authenticated before this step)
        user = request.user  
        
        # Handle resume selection/upload
        pdf_path, error_message, status_code = handle_resume_selection_or_upload(request, user)

        if error_message:
            return JsonResponse({'error': error_message}, status=status_code)

        # Extract form data
        num_questions = int(request.POST['num_questions'])
        language = request.POST['language']
        level = request.POST['level']

        # Process the resume to extract text
        resume_text = extract_text_from_pdf(pdf_path)

        # Generate questions
        response_text = generate_interview_questions(resume_text, "", "", "", "", num_questions, language, level, is_general=True)

        # Clean up if the resume was uploaded
        if request.FILES.get('resume', None):
            try:
                os.remove(pdf_path)
            except FileNotFoundError:
                pass

        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@login_required
@csrf_exempt
def handle_audio_response(request):
    language = request.POST.get('language')
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')

        if not audio_file:
            return JsonResponse({'error': 'No audio file provided.'}, status=400)

        # Save audio file temporarily
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, audio_file.name)

        with open(temp_path, 'wb+') as temp_audio:
            for chunk in audio_file.chunks():
                temp_audio.write(chunk)

        try:
            # Create a Deepgram client using the API key
            deepgram = DeepgramClient(DG_API_KEY)

            # Read the file content
            with open(temp_path, "rb") as file:
                buffer_data = file.read()

            # Prepare the payload (audio data)
            payload = {"buffer": buffer_data}

            # Configure Deepgram options for audio analysis
            options = PrerecordedOptions(
                model="nova-2",
                language="fr",  # Set language as French
                sentiment=True,
            )

            # Call the transcribe_file method with the audio payload and options
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

            # Extract transcription
            transcription = response.to_dict()
            transcript_text = transcription['results']['channels'][0]['alternatives'][0]['transcript']

            # Call Gemini API (or any other AI model) for feedback on the transcription
            gemeni_model_client = GenerativeModelClient()
            feedback_input = f"Provide detailed feedback on the following interview response: {transcript_text} it is important to give feedback in this {language} . Focus on evaluating the technical accuracy, logical flow, and structure of the response. Disregard minor typos or translation issues, and instead, assess whether the answer addresses the question clearly and effectively, demonstrates a solid understanding of the technical concepts, and is well-organized. Provide suggestions to improve the clarity, coherence, and professionalism of the response. Ignorer totalement les fautes de frappe."
            feedback = gemeni_model_client.get_response(feedback_input)

            # Format feedback for better readability
            formatted_feedback = feedback.replace("\n", " ") # Escape certain characters

            # Return the transcription along with formatted feedback as JSON
            return JsonResponse({
                'transcription': transcript_text,
                'feedback': formatted_feedback
            })

        except Exception as e:
            return JsonResponse({'error': f"Exception: {e}"}, status=500)

        finally:
            # Delete temp file
            os.remove(temp_path)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)




def test_interview(request):
    return render(request, 'test_interview.html')
