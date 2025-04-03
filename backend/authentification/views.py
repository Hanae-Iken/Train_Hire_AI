from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, LoginSerializer
from common.models import User, Administrateur, Utilisateur  # Import your custom User model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class SignupView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # The user is created in the serializer
            login(request, user)  # Log the user in after signup
            return Response({"message": "User created and logged in successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = validated_data['user']
            login(request, user)
            return Response({
                "message": "User logged in successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "nom": user.nom, 
                    "prenom": user.prenom 
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    http_method_names = ['head', 'post']
    def post(self, request):
        # User logout
        logout(request)
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
