import html
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from utils.GemeniAiModel import GenerativeModelClient
from django.conf import settings
import PyPDF2
import os


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
                                 skills: str, num_questions: int, language: str, is_general: bool) -> str:
    """
    Generate interview questions based on the provided data.
    If `is_general` is True, skips domain, title, description, and skills.
    """
    # Construct user input based on the type of interview
    if is_general:
        user_input = (f"Generate {num_questions} general interview questions based on the following resume text: {resume_text}. "
                      f"Language of interview: {language}. Give each question on a separate line.")
    else:
        user_input = (f"Generate {num_questions} interview questions based on the following resume text: {resume_text}, "
                      f"job title: {title}, domain: {domain}, job description: {description}, "
                      f"required skills: {skills}. "
                      f"Language of interview: {language}. Give each question on a separate line.")

    # Initialize the model client and get the response
    model_client = GenerativeModelClient()
    response_text = model_client.get_response(user_input)
    return html.unescape(response_text)  # Unescape HTML entities


@csrf_exempt
def gen_personalized_interview(request):
    if request.method == 'POST':
        # Check for required fields
        required_fields = ['resume', 'domain', 'title', 'description', 'skills', 'num_questions', 'language']
        if any(field not in request.POST for field in required_fields if field != 'resume') or 'resume' not in request.FILES:
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        # Extract form data
        resume_file = request.FILES['resume']
        domain = request.POST['domain']
        title = request.POST['title']
        description = request.POST['description']
        skills = request.POST['skills']
        num_questions = int(request.POST['num_questions'])
        language = request.POST['language']

        # Process the resume
        pdf_path = default_storage.save(resume_file.name, resume_file)
        resume_text = extract_text_from_pdf(pdf_path)

        # Generate questions
        response_text = generate_interview_questions(resume_text, domain, title, description, skills, num_questions, language, is_general=False)

        # Clean up
        try:
            os.remove(pdf_path)
        except FileNotFoundError:
            pass

        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def gen_general_interview(request):
    if request.method == 'POST':
        # Check for required fields
        if 'resume' not in request.FILES or 'num_questions' not in request.POST or 'language' not in request.POST:
            return JsonResponse({'error': 'Missing required fields.'}, status=400)

        # Extract form data
        resume_file = request.FILES['resume']
        num_questions = int(request.POST['num_questions'])
        language = request.POST['language']

        # Process the resume
        pdf_path = default_storage.save(resume_file.name, resume_file)
        resume_text = extract_text_from_pdf(pdf_path)

        # Generate questions
        response_text = generate_interview_questions(resume_text, "", "", "", "", num_questions, language, is_general=True)

        # Clean up
        try:
            os.remove(pdf_path)
        except FileNotFoundError:
            pass

        return JsonResponse({'response': response_text})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

