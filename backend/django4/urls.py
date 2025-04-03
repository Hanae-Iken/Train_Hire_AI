"""
URL configuration for django4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from interview_simulation import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('gen_personalized_interview/', views.gen_personalized_interview, name='gen_personalized_interview'),
    path('gen_general_interview/', views.gen_general_interview, name='gen_general_interview'),
    path('handle_audio_response/', views.handle_audio_response, name='handle_audio_response'),
    #path('analyze_feedback/', views.analyze_feedback, name='analyze_feedback'),
    path('test-interview/', views.test_interview, name='test_interview'),
    path('resumes/', include('resumes.urls')),
    #path('test-connection/', views.test_connection, name='test_connection'),
    path('api/', include('authentification.urls')),  # Assuming 'authentification' is your custom app
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token endpoint
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('start_interview/', views.start_interview, name='start_interview'),
    path('analyze_interview/', views.analyze_interview, name='analyze_interview'),
    path('get_questions_for_session/<int:session_id>/', views.get_questions_for_session, name='get_questions_for_session'),
    path('get_previous_interviews/' , views.get_previous_interviews, name='get_previous_interviews'),
    path('get_feedback_details/<int:session_id>/', views.get_feedback_details, name='get_feedback_details'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

