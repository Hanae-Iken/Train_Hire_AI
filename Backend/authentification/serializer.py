from rest_framework import serializers
from common.models import User, Administrateur, Utilisateur, Role  # Import your custom User model
from django.core.exceptions import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'password']

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # role = validated_data.get('role')
        # role = validated_data.get('role', Role.UTILISATEUR)
        # Choose the correct model based on the role
        # if role == 'Admin':
        #     user = Administrateur(**validated_data)
        # elif role == 'Utilisateur':
        #     user = Utilisateur(**validated_data)
        # else:
        #     raise ValidationError('Invalid role')
        validated_data.pop('role', None)  # Ensure any role passed is ignored
        validated_data['role'] = Role.UTILISATEUR 
        user = Utilisateur(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')


        # First, attempt to fetch the user from the base User model
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")

        # Check if the password matches
        if not user.check_password(password):
            raise ValidationError("Invalid credentials")

        # Determine the role of the user dynamically
        if hasattr(user, 'administrateur'):
            role = 'Admin'
        elif hasattr(user, 'utilisateur'):
            role = 'Utilisateur'
        else:
            role = 'Unknown'

        # Return the validated user object and their role
        return {
            'user': user,
            'role': role
        }