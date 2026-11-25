from modeltranslation.translator import register, TranslationOptions
from .models import SiteProfile, Experience, Project, Publication, BlogPost


@register(SiteProfile)
class SiteProfileTranslationOptions(TranslationOptions):
    fields = ("full_name", "headline", "short_bio", "about_markdown", "location")


@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = ("title", "organization", "location", "description_markdown")


@register(Project)
class ProjectTranslationOption(TranslationOptions):
    fields = ("title", "summary", "details_markdown")


@register(Publication)
class PublicationTranslationOptions(TranslationOptions):
    fields = ("title", "venue")


@register(BlogPost)
class BlogPostTranslationOptions(TranslationOptions):
    field = ("title", "excerp", "content_markdown")