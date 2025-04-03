from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Enumération pour les rôles
class Role(models.TextChoices):
    ADMIN = 'Admin', 'Administrateur'
    UTILISATEUR = 'Utilisateur', 'Utilisateur'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.role})"

# Modèles hérités de User
class Administrateur(User):
    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si l'objet est nouveau
            self.role = Role.ADMIN
        super().save(*args, **kwargs)

class Utilisateur(User):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si l'objet est nouveau
            self.role = Role.UTILISATEUR
        super().save(*args, **kwargs)

# Modèle Systeme AI
class SystemeAI(models.Model):
    nomm = models.CharField(max_length=100)
    version = models.FloatField()

    def __str__(self):
        return f"{self.nomm} (v{self.version})"

# Modèle Entretien
# class Entretien(models.Model):
#     type = models.CharField(max_length=100)
#     domaine = models.CharField(max_length=100)
#     systeme_ai = models.ForeignKey(SystemeAI, on_delete=models.CASCADE, related_name='entretiens')

#     def __str__(self):
#         return f"{self.type} - {self.domaine}"

# Modèle CV
class CV(models.Model):
    resume = models.FileField(upload_to='resumes/', null=True, blank=True) 
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='cvs', null=True, blank=True)
    is_selected = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.resume.name} - {'Selected' if self.is_selected else 'Not Selected'}"

# Modèle Questions
# class Question(models.Model):
#     entretien = models.ForeignKey(Entretien, on_delete=models.CASCADE, related_name='questions')
#     contenu = models.TextField()
#     type = models.CharField(max_length=50)

# # Modèle Réponses
# class Reponse(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
#     contenu = models.TextField()
#     score = models.FloatField()

# Modèle Posts
class Post(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='posts')
    domaine = models.CharField(max_length=100)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    competences_requises = models.TextField()

# Modèle Réclamations
class Reclamation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='reclamations')
    administrateur = models.ForeignKey(
        Administrateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reclamations_traitees'
    )
    contenu = models.TextField()

# Modèle Rapport
# class Rapport(models.Model):
#     entretien = models.OneToOneField(Entretien, on_delete=models.CASCADE)
#     score_tech = models.FloatField()
#     score_ling = models.FloatField()
#     score_comport = models.FloatField()
#     suggestion = models.TextField()

class InterviewSession(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)  
    domain = models.CharField(max_length=255, blank=True, null=True) 

class Question(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    audio_file = models.FileField(upload_to='audio_questions/') 
    question_text = models.TextField()
    question_order = models.IntegerField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    audio_file = models.FileField(upload_to='audio_answers/')  # Store the audio file
    transcription = models.TextField(null=True, blank=True)
    facial_expression_data = models.JSONField(null=True, blank=True)


