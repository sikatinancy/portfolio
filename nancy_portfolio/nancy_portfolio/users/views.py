from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods

from .models import (
    Conversation,
    Message,
)

from portfolio.models import (
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)


# ============================================================
# PROFIL
# ============================================================

def get_profile():
    """
    Récupère le profil actif du portfolio.
    """

    return Profile.objects.filter(
        is_active=True,
    ).first()


# ============================================================
# CONNEXION
# ============================================================

def login_view(request):
    """
    Connexion du propriétaire du portfolio.
    """

    if request.user.is_authenticated:
        return redirect(
            "users:dashboard"
        )

    error = None

    if request.method == "POST":

        email = request.POST.get(
            "email",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is not None:

            login(
                request,
                user,
            )

            return redirect(
                "users:dashboard"
            )

        error = "Email ou mot de passe incorrect."

    return render(
        request,
        "auth/login.html",
        {
            "error": error,
        },
    )


# ============================================================
# DECONNEXION
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect(
        "portfolio:home"
    )


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):
    """
    Tableau de bord principal du propriétaire.
    """

    profile = get_profile()

    conversations = (
        Conversation.objects
        .filter(is_archived=False)
        .prefetch_related("messages")
    )

    unread_messages = Message.objects.filter(
        sender__isnull=True,
        is_read=False,
    ).count()

    projects = Project.objects.all()

    skills = Skill.objects.all()

    experiences = Experience.objects.all()

    context = {
        "profile": profile,

        # ==================================================
        # STATISTIQUES
        # ==================================================

        "projects_count": Project.objects.filter(
            is_active=True,
        ).count(),

        "skills_count": Skill.objects.filter(
            is_active=True,
        ).count(),

        "experiences_count": Experience.objects.count(),

        "messages_count": conversations.count(),

        "unread_messages": unread_messages,

        # ==================================================
        # DONNEES CRUD
        # ==================================================

        "projects": projects,

        "skills": skills,

        "experiences": experiences,

        "recent_conversations": conversations[:5],
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


# ============================================================
# PROFIL
# ============================================================

@login_required
@require_http_methods(["GET", "POST"])
def dashboard_profile(request):
    """
    Modification du profil depuis le dashboard.
    """

    profile = get_profile()

    if profile is None:

        profile = Profile.objects.create(
            full_name=(
                request.user.get_full_name()
                or request.user.username
            ),
            profession="",
            short_description="",
            biography="",
            email=request.user.email,
        )

    if request.method == "POST":

        profile.full_name = request.POST.get(
            "full_name",
            profile.full_name,
        )

        profile.profession = request.POST.get(
            "profession",
            profile.profession,
        )

        profile.short_description = request.POST.get(
            "short_description",
            profile.short_description,
        )

        profile.biography = request.POST.get(
            "biography",
            profile.biography,
        )

        profile.email = request.POST.get(
            "email",
            profile.email,
        )

        profile.phone = request.POST.get(
            "phone",
            profile.phone,
        )

        profile.location = request.POST.get(
            "location",
            profile.location,
        )

        profile.github = request.POST.get(
            "github",
            profile.github,
        )

        profile.linkedin = request.POST.get(
            "linkedin",
            profile.linkedin,
        )

        profile.whatsapp = request.POST.get(
            "whatsapp",
            profile.whatsapp,
        )

        if request.FILES.get("profile_image"):

            profile.profile_image = request.FILES[
                "profile_image"
            ]

        if request.FILES.get("cv"):

            profile.cv = request.FILES[
                "cv"
            ]

        profile.save()

        messages.success(
            request,
            "Profil mis à jour avec succès.",
        )

        return redirect(
            "users:dashboard-profile"
        )

    return render(
        request,
        "dashboard/profile.html",
        {
            "profile": profile,
        },
    )


# ============================================================
# CRUD PROJECTS
# ============================================================

@login_required
@require_http_methods(["POST"])
def project_create(request):
    """
    Création d'un projet.
    """

    title = request.POST.get(
        "title",
        "",
    ).strip()

    if not title:

        messages.error(
            request,
            "Le titre du projet est obligatoire.",
        )

        return redirect(
            "users:dashboard"
        )

    slug = slugify(title)

    # Eviter un doublon de slug
    original_slug = slug
    counter = 1

    while Project.objects.filter(
        slug=slug,
    ).exists():

        slug = f"{original_slug}-{counter}"

        counter += 1

    project = Project.objects.create(

        title=title,

        slug=slug,

        short_description=request.POST.get(
            "short_description",
            "",
        ).strip(),

        description=request.POST.get(
            "description",
            "",
        ).strip(),

        technologies=request.POST.get(
            "technologies",
            "",
        ).strip(),

        github_url=request.POST.get(
            "github_url",
            "",
        ).strip(),

        demo_url=request.POST.get(
            "demo_url",
            "",
        ).strip(),

        featured=request.POST.get(
            "featured"
        ) == "on",

        is_active=request.POST.get(
            "is_active"
        ) == "on",
    )

    if request.FILES.get("image"):

        project.image = request.FILES[
            "image"
        ]

        project.save()

    messages.success(
        request,
        "Projet ajouté avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


@login_required
@require_http_methods(["POST"])
def project_update(
    request,
    project_id,
):
    """
    Modification d'un projet.
    """

    project = get_object_or_404(
        Project,
        pk=project_id,
    )

    title = request.POST.get(
        "title",
        "",
    ).strip()

    if not title:

        messages.error(
            request,
            "Le titre du projet est obligatoire.",
        )

        return redirect(
            "users:dashboard"
        )

    project.title = title

    new_slug = slugify(title)

    slug_exists = Project.objects.filter(
        slug=new_slug,
    ).exclude(
        pk=project.pk,
    ).exists()

    if slug_exists:

        new_slug = f"{new_slug}-{project.pk}"

    project.slug = new_slug

    project.short_description = request.POST.get(
        "short_description",
        "",
    ).strip()

    project.description = request.POST.get(
        "description",
        "",
    ).strip()

    project.technologies = request.POST.get(
        "technologies",
        "",
    ).strip()

    project.github_url = request.POST.get(
        "github_url",
        "",
    ).strip()

    project.demo_url = request.POST.get(
        "demo_url",
        "",
    ).strip()

    project.featured = request.POST.get(
        "featured"
    ) == "on"

    project.is_active = request.POST.get(
        "is_active"
    ) == "on"

    if request.FILES.get("image"):

        project.image = request.FILES[
            "image"
        ]

    project.save()

    messages.success(
        request,
        "Projet modifié avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


@login_required
@require_http_methods(["POST"])
def project_delete(
    request,
    project_id,
):
    """
    Suppression d'un projet.
    """

    project = get_object_or_404(
        Project,
        pk=project_id,
    )

    project.delete()

    messages.success(
        request,
        "Projet supprimé avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


# ============================================================
# CRUD COMPETENCES
# ============================================================

@login_required
@require_http_methods(["POST"])
def skill_create(request):
    """
    Création d'une compétence.
    """

    name = request.POST.get(
        "name",
        "",
    ).strip()

    if not name:

        messages.error(
            request,
            "Le nom de la compétence est obligatoire.",
        )

        return redirect(
            "users:dashboard"
        )

    Skill.objects.create(

        name=name,

        category=request.POST.get(
            "category",
            "other",
        ),

        percentage=int(
            request.POST.get(
                "percentage",
                80,
            )
        ),

        icon=request.POST.get(
            "icon",
            "",
        ).strip(),

        description=request.POST.get(
            "description",
            "",
        ).strip(),

        order=int(
            request.POST.get(
                "order",
                0,
            )
        ),

        is_active=request.POST.get(
            "is_active"
        ) == "on",
    )

    messages.success(
        request,
        "Compétence ajoutée avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


@login_required
@require_http_methods(["POST"])
def skill_update(
    request,
    skill_id,
):
    """
    Modification d'une compétence.
    """

    skill = get_object_or_404(
        Skill,
        pk=skill_id,
    )

    skill.name = request.POST.get(
        "name",
        "",
    ).strip()

    skill.category = request.POST.get(
        "category",
        "other",
    )

    skill.percentage = int(
        request.POST.get(
            "percentage",
            80,
        )
    )

    skill.icon = request.POST.get(
        "icon",
        "",
    ).strip()

    skill.description = request.POST.get(
        "description",
        "",
    ).strip()

    skill.order = int(
        request.POST.get(
            "order",
            0,
        )
    )

    skill.is_active = request.POST.get(
        "is_active"
    ) == "on"

    skill.save()

    messages.success(
        request,
        "Compétence modifiée avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


@login_required
@require_http_methods(["POST"])
def skill_delete(
    request,
    skill_id,
):
    """
    Suppression d'une compétence.
    """

    skill = get_object_or_404(
        Skill,
        pk=skill_id,
    )

    skill.delete()

    messages.success(
        request,
        "Compétence supprimée avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


# ============================================================
# CRUD EXPERIENCES
# ============================================================

@login_required
@require_http_methods(["POST"])
def experience_create(request):
    """
    Création d'une expérience.
    """

    company = request.POST.get(
        "company",
        "",
    ).strip()

    position = request.POST.get(
        "position",
        "",
    ).strip()

    if not company or not position:

        messages.error(
            request,
            "L'entreprise et le poste sont obligatoires.",
        )

        return redirect(
            "users:dashboard"
        )

    Experience.objects.create(

        company=company,

        position=position,

        description=request.POST.get(
            "description",
            "",
        ).strip(),

        start_date=request.POST.get(
            "start_date"
        ) or None,

        end_date=request.POST.get(
            "end_date"
        ) or None,

        is_current=request.POST.get(
            "is_current"
        ) == "on",

        location=request.POST.get(
            "location",
            "",
        ).strip(),

        order=int(
            request.POST.get(
                "order",
                0,
            )
        ),
    )

    messages.success(
        request,
        "Expérience ajoutée avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


@login_required
@require_http_methods(["POST"])
def experience_update(
    request,
    experience_id,
):
    """
    Modification d'une expérience.
    """

    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    experience.company = request.POST.get(
        "company",
        "",
    ).strip()

    experience.position = request.POST.get(
        "position",
        "",
    ).strip()

    experience.description = request.POST.get(
        "description",
        "",
    ).strip()

    experience.start_date = request.POST.get(
        "start_date"
    ) or None

    experience.end_date = request.POST.get(
        "end_date"
    ) or None

    experience.is_current = request.POST.get(
        "is_current"
    ) == "on"

    experience.location = request.POST.get(
        "location",
        "",
    ).strip()

    experience.order = int(
        request.POST.get(
            "order",
            0,
        )
    )

    experience.save()

    messages.success(
        request,
        "Expérience modifiée avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


@login_required
@require_http_methods(["POST"])
def experience_delete(
    request,
    experience_id,
):
    """
    Suppression d'une expérience.
    """

    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    experience.delete()

    messages.success(
        request,
        "Expérience supprimée avec succès.",
    )

    return redirect(
        "users:dashboard"
    )


# ============================================================
# MESSAGERIE
# ============================================================

@login_required
def messages_view(request):
    """
    Affiche toutes les conversations reçues.
    """

    conversations = (
        Conversation.objects
        .filter(is_archived=False)
        .prefetch_related("messages")
    )

    return render(
        request,
        "dashboard/messages.html",
        {
            "conversations": conversations,
        },
    )


@login_required
def chat_view(
    request,
    conversation_id,
):
    """
    Affiche une conversation.
    """

    conversation = get_object_or_404(
        Conversation,
        pk=conversation_id,
    )

    messages_list = (
        conversation.messages
        .select_related("sender")
        .all()
    )

    messages_list.filter(
        sender__isnull=True,
        is_read=False,
    ).update(
        is_read=True
    )

    return render(
        request,
        "dashboard/chat.html",
        {
            "conversation": conversation,
            "messages": messages_list,
        },
    )


@login_required
@require_http_methods(["POST"])
def send_message(
    request,
    conversation_id,
):
    """
    Réponse du propriétaire du portfolio.
    """

    conversation = get_object_or_404(
        Conversation,
        pk=conversation_id,
    )

    content = request.POST.get(
        "content",
        "",
    ).strip()

    attachment = request.FILES.get(
        "attachment"
    )

    if not content and not attachment:

        return JsonResponse(
            {
                "success": False,
                "error": "Le message est vide.",
            },
            status=400,
        )

    message_type = "text"

    if attachment:

        content_type = (
            attachment.content_type or ""
        )

        if content_type.startswith("audio/"):

            message_type = "audio"

        elif content_type.startswith("video/"):

            message_type = "video"

        else:

            message_type = "file"

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        content=content,
        attachment=attachment,
        message_type=message_type,
        original_filename=(
            attachment.name
            if attachment
            else ""
        ),
        is_read=True,
    )

    conversation.save(
        update_fields=[
            "updated_at",
        ]
    )

    email_sent = False

    if conversation.visitor_email:

        email_subject = "Réponse à votre message"

        if conversation.subject:

            email_subject = (
                f"Re: {conversation.subject}"
            )

        email_body = (
            f"Bonjour {conversation.visitor_name},\n\n"
            f"{content}\n\n"
            f"Merci pour votre message.\n"
        )

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            to=[
                conversation.visitor_email,
            ],
        )

        if attachment:

            email.attach(
                attachment.name,
                attachment.read(),
                attachment.content_type,
            )

        try:

            email.send(
                fail_silently=False,
            )

            email_sent = True

        except Exception:

            email_sent = False

    return JsonResponse(
        {
            "success": True,
            "message_id": message.id,
            "content": message.content,
            "message_type": message.message_type,
            "attachment": (
                message.attachment.url
                if message.attachment
                else None
            ),
            "email_sent": email_sent,
        }
    )