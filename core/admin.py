from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import SiteProfile, Experience, Project, Publication, ContactMessage, BlogPost


@admin.register(SiteProfile)
class SiteProfileAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("full_name", "enable_telegram_alerts", "enable_email_alerts", "updated_at")
    list_editable = ("enable_telegram_alerts", "enable_email_alerts")


@admin.register(Experience)
class ExperienceAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "organization", "role_type", "start_date", "end_date", "order", "is_visible")
    list_filter = ("role_type", "is_visible")
    list_editable = ("order", "is_visible")


@admin.register(Project)
class ProjectAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "category", "is_featured", "order")
    list_filter = ("category", "is_featured")
    list_editable = ("is_featured", "order")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Publication)
class PublicationAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "venue", "year", "is_visible")
    list_filter = ("year", "is_visible")
    list_editable = ("is_visible",)


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("title", "is_published", "published_at", "updated_at")
    list_filter = ("is_published", "published_at")
    list_editable = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "content_markdown", "tags")


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ("sender_name", "sender_email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("sender_name", "sender_email", "subject", "message", "created_at")