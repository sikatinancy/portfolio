from django.contrib import admin

from .models import (
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SocialLink,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "profession",
        "email",
        "phone",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "full_name",
        "email",
        "profession",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "percentage",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "order",
        "name",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "featured",
        "is_active",
    )

    search_fields = (
        "title",
        "short_description",
        "description",
        "technologies",
    )

    prepopulated_fields = {
        "slug": (
            "title",
        ),
    }


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "position",
        "company",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "is_current",
        "company",
    )

    search_fields = (
        "position",
        "company",
        "description",
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "degree",
        "institution",
        "start_date",
        "end_date",
    )

    list_filter = (
        "institution",
    )

    search_fields = (
        "degree",
        "institution",
        "description",
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "url",
    )

    ordering = (
        "order",
    )