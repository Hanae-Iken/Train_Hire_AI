from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

class InterviewSimulationTests(APITestCase):

    def setUp(self):
        """Créer un utilisateur de test pour l'authentification."""
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_personalized_interview_endpoint(self):
        """Test l'accès à l'endpoint de génération d'entretien personnalisé."""
        url = reverse('gen_personalized_interview')
        response = self.client.post(url, {
            "domain": "IT",
            "title": "Software Engineer",
            "description": "Develop and maintain software",
            "skills": "Python, Django",
            "num_questions": 5,
            "language": "English",
            "level": "Intermediate"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("response", response.data)  # Vérifie que la réponse contient un champ "response"

    def test_general_interview_endpoint(self):
        """Test l'accès à l'endpoint de génération d'entretien général."""
        url = reverse('gen_general_interview')
        response = self.client.post(url, {
            "num_questions": 5,
            "language": "English",
            "level": "Intermediate"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("response", response.data)
