from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse  # Utilisation de reverse pour éviter les erreurs d’URL

User = get_user_model()

class AuthenticationTests(APITestCase):

    def setUp(self):
        """Création d'un utilisateur de test avant d'exécuter les tests."""
        self.user_data = {
            "nom": "Test",
            "prenom": "User",
            "email": "test@example.com",
            "password": "password123"
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user(self):
        """Test d'inscription d'un nouvel utilisateur."""
        url = reverse('signup')  # Assure-toi que ce nom est bien défini dans urls.py
        new_user_data = {
            "nom": "New",
            "prenom": "User",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_valid_user(self):
        """Test de connexion avec un utilisateur existant."""
        url = reverse('signin')  # Assure-toi que ce nom est bien défini dans urls.py
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)  # Vérifie que la réponse contient bien un message

    def test_login_invalid_user(self):
        """Test de connexion avec des identifiants incorrects."""
        url = reverse('signin')
        wrong_login_data = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, wrong_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)  # Vérifie que la réponse contient une erreur
