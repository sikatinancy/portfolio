from django.urls import path

from . import views


app_name = "users"


urlpatterns = [

    # ==================================================
    # AUTHENTIFICATION
    # ==================================================

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),


    # ==================================================
    # DASHBOARD
    # ==================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "dashboard/profile/",
        views.dashboard_profile,
        name="dashboard-profile",
    ),


    # ==================================================
    # PROJECTS
    # ==================================================

    path(
        "dashboard/projects/create/",
        views.project_create,
        name="project-create",
    ),

    path(
        "dashboard/projects/<int:project_id>/update/",
        views.project_update,
        name="project-update",
    ),

    path(
        "dashboard/projects/<int:project_id>/delete/",
        views.project_delete,
        name="project-delete",
    ),


    # ==================================================
    # COMPETENCES
    # ==================================================

    path(
        "dashboard/skills/create/",
        views.skill_create,
        name="skill-create",
    ),

    path(
        "dashboard/skills/<int:skill_id>/update/",
        views.skill_update,
        name="skill-update",
    ),

    path(
        "dashboard/skills/<int:skill_id>/delete/",
        views.skill_delete,
        name="skill-delete",
    ),


    # ==================================================
    # EXPERIENCES
    # ==================================================

    path(
        "dashboard/experiences/create/",
        views.experience_create,
        name="experience-create",
    ),

    path(
        "dashboard/experiences/<int:experience_id>/update/",
        views.experience_update,
        name="experience-update",
    ),

    path(
        "dashboard/experiences/<int:experience_id>/delete/",
        views.experience_delete,
        name="experience-delete",
    ),


    # ==================================================
    # MESSAGERIE
    # ==================================================

    path(
        "dashboard/messages/",
        views.messages_view,
        name="messages",
    ),

    path(
        "dashboard/messages/<int:conversation_id>/",
        views.chat_view,
        name="chat",
    ),

    path(
        "dashboard/messages/<int:conversation_id>/send/",
        views.send_message,
        name="send-message",
    ),
]