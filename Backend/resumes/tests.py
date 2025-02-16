from django.urls import path
from resumes import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('list/', views.list_resumes, name='list_resumes'),
    path('view/<int:resume_id>/', views.view_resume, name='view_resume'),
]

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from common.models import CV
import os

@login_required
@csrf_exempt
def upload_resume(request):
    if request.method == 'POST':
        user = request.user
        resume_file = request.FILES.get('resume')

        if not resume_file:
            return JsonResponse({'error': 'No resume file uploaded.'}, status=400)

        existing_resume = CV.objects.filter(utilisateur=user, resume=resume_file.name).first()
        if existing_resume:
            return JsonResponse({'error': 'This resume has already been uploaded.'}, status=400)

        new_resume = CV.objects.create(utilisateur=user, resume=resume_file)
        if not CV.objects.filter(utilisateur=user, is_selected=True).exists():
            new_resume.is_selected = True
            new_resume.save()

        return JsonResponse({'success': 'Resume uploaded successfully.', 'resume_id': new_resume.id})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def delete_resume(request, resume_id):
    if request.method == 'POST':
        user = request.user
        resume = get_object_or_404(CV, id=resume_id, utilisateur=user)
        resume.resume.delete()
        resume.delete()
        return JsonResponse({'success': 'Resume deleted successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
@csrf_exempt
def list_resumes(request):
    user = request.user
    resumes = CV.objects.filter(utilisateur=user).values('id', 'resume', 'is_selected', 'uploaded_at')
    return JsonResponse({'resumes': list(resumes)})

@login_required
@csrf_exempt
def view_resume(request, resume_id):
    user = request.user
    resume = get_object_or_404(CV, id=resume_id, utilisateur=user)
    file_path = resume.resume.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{resume.resume.name}"'
        return response
    return JsonResponse({'error': 'File not found.'}, status=404)
