from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """
    Informations principales du propriétaire du portfolio.
    """

    full_name = models.CharField(
        max_length=150,
    )

    profession = models.CharField(
        max_length=200,
    )

    short_description = models.TextField(
        blank=True,
    )

    biography = models.TextField(
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
    )

    cv = models.FileField(
        upload_to="cv/",
        blank=True,
        null=True,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    github = models.URLField(
        blank=True,
    )

    linkedin = models.URLField(
        blank=True,
    )

    whatsapp = models.URLField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    """
    Compétence professionnelle.
    """

    CATEGORY_CHOICES = [
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("database", "Base de données"),
        ("tools", "Outils"),
        ("other", "Autre"),
    ]

    name = models.CharField(
        max_length=100,
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
    )

    percentage = models.PositiveIntegerField(
        default=80,
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "order",
            "name",
        ]

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Projet présenté dans le portfolio.
    """

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        unique=True,
    )

    short_description = models.TextField(
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
    )

    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Séparer les technologies par des virgules.",
    )

    github_url = models.URLField(
        blank=True,
    )

    demo_url = models.URLField(
        blank=True,
    )

    featured = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-featured",
            "-created_at",
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "portfolio:project_detail",
            kwargs={
                "slug": self.slug,
            },
        )

    def technology_list(self):
        return [
            technology.strip()
            for technology in self.technologies.split(",")
            if technology.strip()
        ]


class Experience(models.Model):
    """
    Expérience professionnelle.
    """

    company = models.CharField(
        max_length=200,
    )

    position = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    # Nullable pour permettre la migration des anciennes données.
    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    location = models.CharField(
        max_length=150,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = [
            "-start_date",
            "order",
        ]

    def __str__(self):
        return f"{self.position} - {self.company}"


class Education(models.Model):
    """
    Formation académique.
    """

    institution = models.CharField(
        max_length=200,
    )

    degree = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    # Nullable pour éviter le problème de migration
    # avec les anciennes formations déjà enregistrées.
    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = [
            "-start_date",
        ]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class SocialLink(models.Model):
    """
    Lien vers un réseau social ou une plateforme.
    """

    name = models.CharField(
        max_length=100,
    )

    url = models.URLField()

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = [
            "order",
        ]

    def __str__(self):
        return self.name