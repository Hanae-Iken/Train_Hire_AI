from django.urls import path
from resumes import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    # path('select/<int:resume_id>/', views.select_resume, name='select_resume'),
    path('list/', views.list_resumes, name='list_resumes'),
    path('view/<int:resume_id>/', views.view_resume, name='view_resume'),
]
