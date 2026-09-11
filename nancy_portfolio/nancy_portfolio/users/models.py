from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Utilisateur du portfolio.

    L'adresse e-mail est utilisée comme identifiant
    principal pour la connexion.
    """

    email = models.EmailField(
        unique=True,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username",
    ]

    objects = UserManager()

    def __str__(self):
        return self.email


class Conversation(models.Model):
    """
    Conversation entre le propriétaire du portfolio
    et un visiteur ou un client.
    """

    visitor_name = models.CharField(
        max_length=150,
    )

    visitor_email = models.EmailField()

    visitor_phone = models.CharField(
        max_length=50,
        blank=True,
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    is_archived = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = [
            "-updated_at",
        ]

    def __str__(self):
        return (
            f"{self.visitor_name} - "
            f"{self.subject or 'Sans sujet'}"
        )


class Message(models.Model):
    """
    Message appartenant à une conversation.

    sender=None :
        message envoyé par le visiteur depuis
        le formulaire public.

    sender=request.user :
        réponse envoyée depuis le dashboard.
    """

    MESSAGE_TYPES = [
        ("text", "Texte"),
        ("audio", "Audio"),
        ("video", "Vidéo"),
        ("file", "Fichier"),
        ("folder", "Dossier"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
    )

    content = models.TextField(
        blank=True,
    )

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES,
        default="text",
    )

    attachment = models.FileField(
        upload_to="attachments/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Message #{self.pk}"


class Notification(models.Model):
    """
    Notification destinée au propriétaire
    du portfolio dans le dashboard.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"Notification #{self.pk}"