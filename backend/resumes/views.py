from django.shortcuts import render
from django.http import JsonResponse,FileResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from common.models import CV,Utilisateur,AbstractBaseUser,BaseUserManager,CustomUserManager
import os
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def upload_resume(request):
    if request.method == 'POST':
        # user = request.user
        # Test below with a manually inserted id before testing with authentification
        # user = Utilisateur.objects.get(id=1)
        user = request.user  
        resume_file = request.FILES.get('resume')

        if not resume_file:
            return JsonResponse({'error': 'No resume file uploaded.'}, status=400)

        # Check if the uploaded resume already exists
        existing_resume = CV.objects.filter(utilisateur=user, resume=resume_file.name).first()
        
        if existing_resume:
            return JsonResponse({'error': 'This resume has already been uploaded.'}, status=400)

        # Store the new resume
        new_resume = CV.objects.create(utilisateur=user, resume=resume_file)
        
        # If this is the first resume uploaded or a new resume, set it as selected
        if not CV.objects.filter(utilisateur=user, is_selected=True).exists():
            new_resume.is_selected = True
            new_resume.save()
        
        return JsonResponse({'success': 'Resume uploaded successfully.', 'resume_id': new_resume.id})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def delete_resume(request, resume_id):
    if request.method == 'POST':
        # user = request.user
        # Test below with a manually inserted id before testing with authentification
        # user = Utilisateur.objects.get(id=1)
        user = request.user  
        try:
            resume = CV.objects.get(id=resume_id, utilisateur=user)
            resume.resume.delete()  # Deletes the file from storage
            resume.delete()
            return JsonResponse({'success': 'Resume deleted successfully.'})
        except CV.DoesNotExist:
            return JsonResponse({'error': 'Resume not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

# @csrf_exempt
# def select_resume(request, resume_id):
#     if request.method == 'POST':
#         # user = request.user
#         # Test below with a manually inserted id before testing with authentification
#         user = Utilisateur.objects.get(id=1)
#         try:
#             # Mark all other resumes as not selected
#             CV.objects.filter(utilisateur=user).update(is_selected=False)

#             # Mark the selected resume
#             selected_resume = CV.objects.get(id=resume_id, utilisateur=user)
#             selected_resume.is_selected = True
#             selected_resume.save()

#             return JsonResponse({'success': f'Resume {selected_resume.resume.name} is now selected for interviews.'})
#         except CV.DoesNotExist:
#             return JsonResponse({'error': 'Resume not found.'}, status=404)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def list_resumes(request):
    # user = request.user
    # Test below with a manually inserted id before testing with authentification
    # user = Utilisateur.objects.get(id=1)
    user = request.user  
    resumes = CV.objects.filter(utilisateur=user).values('id', 'resume', 'is_selected', 'uploaded_at')

    return JsonResponse({'resumes': list(resumes)})

@login_required
@csrf_exempt
def view_resume(request, resume_id):
    # user = request.user
    # Test below with a manually inserted id before testing with authentification
    # user = Utilisateur.objects.get(id=1)
    user = request.user  
    try:
        # Fetch the specific resume by its ID for the given user
        resume = CV.objects.get(id=resume_id, utilisateur=user)
        # Get the file path
        file_path = resume.resume.path  
        # Check if the file exists
        if os.path.exists(file_path):
            # Open and return the file as a response (this will trigger a download in most browsers)
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # Change the MIME type if necessary
            response['Content-Disposition'] = f'inline; filename="{resume.resume.name}"'  # Inline to view, attachment to download
            return response
        else:
            return JsonResponse({'error': 'File not found.'}, status=404)
    except CV.DoesNotExist:
        return JsonResponse({'error': 'Resume not found.'}, status=404)

