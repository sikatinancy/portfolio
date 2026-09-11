from django.urls import path

from . import views


app_name = "portfolio"


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "about/",
        views.about,
        name="about",
    ),

    path(
        "projects/",
        views.projects,
        name="projects",
    ),

    path(
        "projects/<slug:slug>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
        "skills/",
        views.skills,
        name="skills",
    ),

    path(
        "experiences/",
        views.experiences,
        name="experiences",
    ),

    path(
        "contact/",
        views.contact,
        name="contact",
    ),
]