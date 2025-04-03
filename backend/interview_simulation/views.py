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
from common.models import CV, Utilisateur, AbstractBaseUser, BaseUserManager, CustomUserManager,InterviewSession,Question,Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import logging
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from textblob import TextBlob
import logging
from dotenv import load_dotenv
import tempfile
load_dotenv(dotenv_path= "django4/.env")
DG_API_KEY = os.getenv('DG_API_KEY')
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
    SpeakOptions
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

@login_required(login_url='/api/signin/')
@csrf_exempt
def start_interview(request):
    if request.method == 'POST':
        user = request.user
        session = InterviewSession.objects.create(utilisateur=user)
        request.session['interview_session_id'] = session.id
        return JsonResponse({'status': 'Interview started', 'session_id': session.id})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def generate_interview_questions(resume_text: str, domain: str, title: str, description: str, 
                                 skills: str, num_questions: int, language: str, level: str, is_general: bool) -> list:
    """
    Generate interview questions based on the provided data.
    Returns a list of dictionaries, where each dictionary represents a question.
    """
    if is_general:
        user_input = (f"Generate {num_questions} general interview questions.Start with self introduction questions. Include a mix of questions: some based on the following resume text: {resume_text}, "
                      f"and others unrelated to the resume. "
                      f"Include questions about soft skills. "
                      f"Language of interview: {language}, difficulty level: {level}. "
                      f"Return the results as a list of dictionaries, where each dictionary contains 'type', 'question', and 'difficulty' keys.")
    else:
        user_input = (f"Generate {num_questions} interview questions.Start with self introduction questions. Include a mix of questions: some based on the following resume text: {resume_text}, "
                      f"job title: {title}, domain: {domain}, job description: {description}, "
                      f"required skills: {skills}, "
                      f"and others unrelated to the resume or job. "
                      f"Include questions about soft skills. "
                      f"Language of interview: {language}, difficulty level: {level}. "
                      f"Return the results as a list of dictionaries, where each dictionary contains 'type', 'question', and 'difficulty' keys.")

    model_client = GenerativeModelClient()
    response_text = model_client.get_response(user_input)
    
    # Unescape HTML and extract JSON
    clean_response = html.unescape(response_text).strip()
    if clean_response.startswith("```json"):
        clean_response = clean_response[7:-3].strip() 

    try:
        return json.loads(clean_response)  # Ensure the response is a list of dictionaries
    except json.JSONDecodeError:
        return [{"error": "Failed to parse AI response as JSON."}]





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



def text_to_speech(text, question_id):
    try:
        # Initialize Deepgram client
        deepgram = DeepgramClient(DG_API_KEY)

        # Set options for the speech synthesis
        options = SpeakOptions(
            model="aura-asteria-en",  # Choose the desired voice model
        )

        # Generate a unique filename for the audio file
        audio_filename = f"question_{question_id}.mp3"
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio_questions', audio_filename)

        # Ensure the 'audio_questions' directory exists
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)

        # Convert text to speech and save the audio file
        response = deepgram.speak.v("1").save(audio_path, {"text": text}, options)

        # Check if the response contains the correct audio file
        if response is not None:
            return audio_path  # Return the path as a string
        else:
            print("Failed to generate audio.")
            return None

    except Exception as e:
        print(f"Exception in text_to_speech: {e}")
        return None


from django.core.files import File
import os



logger = logging.getLogger(__name__)

from django.core.files.base import ContentFile
import os



LANGUAGE_MAPPING = {
    'English': 'en',
    'French': 'fr',
}
@login_required(login_url='/api/signin/')
@csrf_exempt
def gen_personalized_interview(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('/api/signin/')  
        return JsonResponse({'error': 'Method "GET" not allowed. Only POST requests are accepted.'}, status=405)

    if request.method == 'POST':
        user = request.user
        logger.info("User: %s", user)

        if not isinstance(user, Utilisateur):
            return JsonResponse({'error': 'Unauthorized user type.'}, status=403)

        # Extract form data
        domain = request.POST.get('domain')
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')
        num_questions = 10  # Fixed number of questions
        language = request.POST.get('language')  # User-selected language
        level = request.POST.get('level')

        # Create a new interview session with title and domain
        session = InterviewSession.objects.create(
            utilisateur=user,
            title=title,
            domain=domain
        )
        request.session['interview_session_id'] = session.id
        request.session['language'] = language

        # Handle resume selection or upload
        pdf_path, error_message, status_code = handle_resume_selection_or_upload(request, user)
        if error_message:
            return JsonResponse({'error': error_message}, status=status_code)

        # Process the resume to extract text
        resume_text = extract_text_from_pdf(pdf_path)

        # Generate questions
        questions = generate_interview_questions(
            resume_text, domain, title, description, skills, num_questions, language, level, is_general=False
        )

        # Ensure questions exist
        if not questions:
            return JsonResponse({'error': 'No questions generated.'}, status=500)

        # Store all questions in the database and prepare the response
        question_list = []
        for i, question_data in enumerate(questions):
            question_text = question_data.get('question', '')
            question_obj = Question.objects.create(
                session=session,
                question_text=question_text,
                question_order=i
            )

            # Prepare question data for the response
            question_dict = {
                'question_id': question_obj.id,
                'question': question_text,
                'question_order': i,
                'audio_url': None  # Default value
            }

            # Only convert text to speech if the language is English
            if language.lower() == 'english':
                audio_url = text_to_speech(question_text, question_obj.id)
                if audio_url:
                    # Save the audio file path to the database
                    with open(audio_url, 'rb') as audio_file:
                        question_obj.audio_file.save(
                            os.path.basename(audio_url),
                            ContentFile(audio_file.read()),
                            save=True
                        )
                    question_dict['audio_url'] = question_obj.audio_file.url

            question_list.append(question_dict)

        # Return all questions in the response
        return JsonResponse({'questions': question_list ,'session_id': session.id})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@login_required(login_url='/api/signin/')
@csrf_exempt
def gen_general_interview(request):
    if request.method == 'POST':
        user = request.user
        logger.info("User: %s", user)

        # Ensure the user is of the correct type (if needed)
        if not isinstance(user, Utilisateur):
            return JsonResponse({'error': 'Unauthorized user type.'}, status=403)

        # Create a new interview session
        session = InterviewSession.objects.create(utilisateur=user)
        request.session['interview_session_id'] = session.id

        # Handle resume selection or upload
        pdf_path, error_message, status_code = handle_resume_selection_or_upload(request, user)
        if error_message:
            return JsonResponse({'error': error_message}, status=status_code)

        # Extract form data
        num_questions = 15  # Fixed number of questions
        language = request.POST.get('language')  # User-selected language
        level = request.POST.get('level')

        # Store the selected language in the session
        request.session['language'] = language

        # Process the resume to extract text
        resume_text = extract_text_from_pdf(pdf_path)

        # Generate general questions
        questions = generate_interview_questions(
            resume_text, "", "", "", "", num_questions, language, level, is_general=True
        )

        # Ensure questions exist
        if not questions:
            return JsonResponse({'error': 'No questions generated.'}, status=500)

        # Store all questions in the database and prepare the response
        question_list = []
        for i, question_data in enumerate(questions):
            question_text = question_data.get('question', '')
            question_obj = Question.objects.create(
                session=session,
                question_text=question_text,
                question_order=i
            )

            # Prepare question data for the response
            question_dict = {
                'question_id': question_obj.id,
                'question': question_text,
                'question_order': i,
                'audio_url': None  # Default value
            }

            # Only convert text to speech if the language is English
            if language.lower() == 'english':
                audio_url = text_to_speech(question_text, question_obj.id)
                if audio_url:
                    # Save the audio file path to the database
                    with open(audio_url, 'rb') as audio_file:
                        question_obj.audio_file.save(
                            os.path.basename(audio_url),
                            ContentFile(audio_file.read()),
                            save=True
                        )
                    question_dict['audio_url'] = question_obj.audio_file.url

            question_list.append(question_dict)

        # Return all questions in the response
        return JsonResponse({'questions': question_list, 'session_id': session.id})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)





@login_required(login_url='/api/signin/')
@csrf_exempt
def handle_audio_response(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        question_id = request.POST.get('question_id')  # Get the question ID from the request

        if not audio_file:
            return JsonResponse({'error': 'No audio file provided.'}, status=400)

        try:
            # Save the audio file to the database
            question = Question.objects.get(id=question_id)  # Retrieve the corresponding question
            answer = Answer.objects.create(
                question=question,
                audio_file=audio_file,  # Store the audio file directly
            )

            return JsonResponse({
                'success': 'Answer recorded successfully.',
                'answer_id': answer.id  # Optionally return the answer ID
            })

        except Question.DoesNotExist:
            return JsonResponse({'error': 'Question not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f"Exception: {e}"}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



import json
import re



import json
import re

@login_required(login_url='/api/signin/')
@csrf_exempt
def analyze_interview(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    session_id = request.session.get('interview_session_id')
    print(f"Session ID from request: {session_id}")

    if not session_id:
        return JsonResponse({'error': 'No active interview session.'}, status=400)

    try:
        session = InterviewSession.objects.get(id=session_id)
        questions = session.questions.all()
        print(f"Number of questions found: {questions.count()}")

        # Get the language from the session
        # language_name = request.POST.get('language', 'English')  
        language_name = request.session.get('language', 'English')
        language_code = LANGUAGE_MAPPING.get(language_name, 'en')  # Map to language code
        print(f"Selected language: {language_name} -> {language_code}")

        feedback_results = []

        for question in questions:
            answer = question.answers.first()

            if not answer or not answer.audio_file:
                feedback_results.append({
                    'question_id': question.id,
                    'question_text': question.question_text,
                    'transcription': "",
                    'feedback': {"error": "No audio file provided."},
                })
                continue

            audio_file_path = answer.audio_file.path
            print(f"Audio file path: {audio_file_path}")

            # Deepgram transcription
            try:
                deepgram = DeepgramClient(DG_API_KEY)
                with open(audio_file_path, "rb") as file:
                    buffer_data = file.read()

                payload = {"buffer": buffer_data}
                options = PrerecordedOptions(
                    model="nova-2",
                    language=language_code,  # Use the mapped language code
                    sentiment=True,
                )
                
                response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
                transcription = response.to_dict()
                transcript_text = transcription.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', "")
            except Exception as e:
                print(f"Deepgram transcription error: {e}")
                transcript_text = ""

            answer.transcription = transcript_text
            answer.save()

            # Gemini feedback
            try:
                gemeni_model_client = GenerativeModelClient()
                feedback_input = f"""
                Analyze in detail and provide structured feedback in **{language_name}** in JSON format. Focus on:
                - Strengths
                - Weaknesses
                - Suggestions for Improvement
                - Technical Details
                
                Response: {transcript_text}
                
                Format the feedback as:
                {{
                    "strengths": "List strengths.",
                    "weaknesses": "List weaknesses.",
                    "suggestionsForImprovement": "Provide suggestions.",
                    "technicalDetails": "Evaluate technical accuracy."
                }}
                """
                feedback = gemeni_model_client.get_response(feedback_input)
                feedback = re.sub(r'^```json\n', '', feedback)
                feedback = re.sub(r'\n```$', '', feedback)
                feedback = json.loads(feedback)
            except Exception as e:
                print(f"Gemini API error: {e}")
                feedback = {"error": "Feedback generation failed."}

            feedback_results.append({
                'question_id': question.id,
                'question_text': question.question_text,
                'transcription': transcript_text,
                'feedback': feedback,
            })

        session.feedback = json.dumps(feedback_results)
        session.save()
        return JsonResponse({'feedback_results': feedback_results})

    except InterviewSession.DoesNotExist:
        return JsonResponse({'error': 'Interview session not found.'}, status=404)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return JsonResponse({'error': f"Unexpected error: {e}"}, status=500)




@login_required(login_url='/api/signin/')
@csrf_exempt
def get_questions_for_session(request, session_id):
    if request.method == 'GET':
        try:
            session = InterviewSession.objects.get(id=session_id)
            questions = session.questions.all().order_by('question_order')

            question_list = []
            for question in questions:
                question_data = {
                    'question_id': question.id,
                    'question_text': question.question_text,
                    'audio_url': question.audio_file.url if question.audio_file else None,
                    'question_order': question.question_order,
                }
                question_list.append(question_data)

            return JsonResponse({'questions': question_list}, status=200)
        except InterviewSession.DoesNotExist:
            return JsonResponse({'error': 'Interview session not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@csrf_exempt
@login_required(login_url='/api/signin/')
def get_previous_interviews(request):
    if request.method == 'GET':
        user = request.user
        sessions = InterviewSession.objects.filter(utilisateur=user).order_by('-start_time')

        session_list = []
        for session in sessions:
            try:
                feedback_results = json.loads(session.feedback) if session.feedback else []
            except json.JSONDecodeError:
                feedback_results = []

            session_list.append({
                'session_id': session.id,
                'created_at': session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'title': session.title if session.title else 'Unknown Title',  # Get title from session object
                'domain': session.domain if session.domain else 'Unknown Domain',  # Get domain from session object
                'questions': feedback_results,  # Contains question_id, question_text, transcription, and feedback
            })

        return JsonResponse({'sessions': session_list}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



@login_required(login_url='/api/signin/')
@csrf_exempt
def get_feedback_details(request, session_id):
    if request.method == 'GET':
        try:
            session = InterviewSession.objects.get(id=session_id)
            feedback_results = json.loads(session.feedback) if session.feedback else []

            return JsonResponse({
                'session_id': session.id,
                'created_at': session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'title': request.session.get('title', 'Unknown Title'),
                'domain': request.session.get('domain', 'Unknown Domain'),
                'questions': feedback_results,
            }, status=200)
        except InterviewSession.DoesNotExist:
            return JsonResponse({'error': 'Interview session not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def test_interview(request):
    return render(request, 'test_interview.html')
