from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from portfolio.models import (
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SocialLink,
)


from nancy_portfolio.users.models import (
    Conversation,
    Message,
)


def get_profile():
    """
    Récupère le profil actif du portfolio.
    """

    return Profile.objects.filter(
        is_active=True,
    ).first()


def home(request):
    profile = get_profile()

    featured_projects = Project.objects.filter(
        is_active=True,
        featured=True,
    )[:6]

    skills = Skill.objects.filter(
        is_active=True,
    )[:8]

    experiences = Experience.objects.all()[:3]

    return render(
        request,
        "pages/home.html",
        {
            "profile": profile,
            "featured_projects": featured_projects,
            "skills": skills,
            "experiences": experiences,
        },
    )


def about(request):
    profile = get_profile()

    experiences = Experience.objects.all()

    education = Education.objects.all()

    return render(
        request,
        "pages/about.html",
        {
            "profile": profile,
            "experiences": experiences,
            "education": education,
        },
    )


def projects(request):
    project_list = Project.objects.filter(
        is_active=True,
    )

    return render(
        request,
        "pages/projects.html",
        {
            "projects": project_list,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(
        Project,
        slug=slug,
        is_active=True,
    )

    return render(
        request,
        "pages/project-detail.html",
        {
            "project": project,
        },
    )


def skills(request):
    skill_list = Skill.objects.filter(
        is_active=True,
    )

    return render(
        request,
        "pages/skills.html",
        {
            "skills": skill_list,
        },
    )


def experiences(request):
    experience_list = Experience.objects.all()

    education = Education.objects.all()

    return render(
        request,
        "pages/experiences.html",
        {
            "experiences": experience_list,
            "education": education,
        },
    )


def contact(request):
    """
    Formulaire de contact public.

    Le visiteur peut envoyer :
    - son nom
    - son adresse e-mail
    - son numéro de téléphone
    - son sujet
    - son message

    Une Conversation est créée dans l'application users.

    Le premier Message de la conversation est créé avec
    sender=None car le visiteur n'est pas connecté.

    La conversation apparaîtra ensuite dans le dashboard.
    """

    profile = get_profile()

    if request.method == "POST":

        visitor_name = request.POST.get(
            "name",
            "",
        ).strip()

        visitor_email = request.POST.get(
            "email",
            "",
        ).strip()

        visitor_phone = request.POST.get(
            "phone",
            "",
        ).strip()

        subject = request.POST.get(
            "subject",
            "",
        ).strip()

        content = request.POST.get(
            "message",
            "",
        ).strip()

        if not visitor_name:
            messages.error(
                request,
                "Veuillez renseigner votre nom.",
            )

            return render(
                request,
                "pages/contact.html",
                {
                    "profile": profile,
                },
            )

        if not visitor_email:
            messages.error(
                request,
                "Veuillez renseigner votre adresse e-mail.",
            )

            return render(
                request,
                "pages/contact.html",
                {
                    "profile": profile,
                },
            )

        if not content:
            messages.error(
                request,
                "Veuillez renseigner votre message.",
            )

            return render(
                request,
                "pages/contact.html",
                {
                    "profile": profile,
                },
            )

        conversation = Conversation.objects.create(
            visitor_name=visitor_name,
            visitor_email=visitor_email,
            visitor_phone=visitor_phone,
            subject=subject,
        )

        Message.objects.create(
            conversation=conversation,
            sender=None,
            content=content,
            message_type="text",
            is_read=False,
        )

        messages.success(
            request,
            "Votre message a bien été envoyé.",
        )

        return redirect(
            "portfolio:contact"
        )

    return render(
        request,
        "pages/contact.html",
        {
            "profile": profile,
        },
    )