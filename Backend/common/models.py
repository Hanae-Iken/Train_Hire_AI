from django.db import models

# Enumération pour les rôles
class Role(models.TextChoices):
    ADMIN = 'Admin', 'Administrateur'
    UTILISATEUR = 'Utilisateur', 'Utilisateur'

# Modèle User
class User(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mdp = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=Role.choices)

    def _str_(self):
        return f"{self.nomm} {self.prenom} ({self.role})"

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

    def _str_(self):
        return f"{self.nom} (v{self.version})"

# Modèle Entretien
class Entretien(models.Model):
    type = models.CharField(max_length=100)
    domaine = models.CharField(max_length=100)
    systeme_ai = models.ForeignKey(SystemeAI, on_delete=models.CASCADE, related_name='entretiens')

    def _str_(self):
        return f"{self.type} - {self.domaine}"

# Modèle CV
class CV(models.Model):
    contenu = models.TextField()
    systeme_ai = models.ForeignKey(SystemeAI, on_delete=models.CASCADE, related_name='cvs')

    def _str_(self):
        return f"CV {self.id}"

# Modèle Questions
class Question(models.Model):
    entretien = models.ForeignKey(Entretien, on_delete=models.CASCADE, related_name='questions')
    contenu = models.TextField()
    type = models.CharField(max_length=50)

# Modèle Réponses
class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    contenu = models.TextField()
    score = models.FloatField()

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
class Rapport(models.Model):
    entretien = models.OneToOneField(Entretien, on_delete=models.CASCADE)
    score_tech = models.FloatField()
    score_ling = models.FloatField()
    score_comport = models.FloatField()
    suggestion = models.TextField()

