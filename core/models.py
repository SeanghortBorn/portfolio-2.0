import math
from django.db import models
from django.core.exceptions import ValidationError


class SiteProfile(models.Model):
    """Singleon model for global profile content AND notification switches"""
    full_name = models.CharField(max_length=120, default="Born Seanghort")
    headline = models.CharField(max_length=255)
    short_bio = models.TextField(help_text="Short introduction in the hero banner.")
    about_markdown = models.TextField(
        blank=True,
        help_text="Supports full Markdown (**bold**, lists, links, and code blocks)."
    )
    location = models.CharField(max_length=120, default="Phnom Penh, Cambodia")
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True)
    resume_pdf = models.FileField(upload_to="docs/", blank=True, null=True)

    # Social Links (Language-Independent)
    github_url = models.URLField(blank=True)
    orcid_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # Dynamic notification toggles (Enable/Disable easily form the Admin UI!)
    enable_telegram_alerts = models.BooleanField(
        default=True,
        help_text="Send an instant Telegram bot message when someone submits the contact form."
    )
    enable_email_alerts = models.BooleanField(
        default=True,
        help_text="Send an email alert when someone submits the contact form."
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and SiteProfile.objects.exists():
            raise ValidationError('Only one SiteProfile instance is allowed')
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Site Configuration ({self.full_name})"

    class Meta:
        verbose_name = "Site Profile & Notification Settings" 
        verbose_name_plural = "Site Profile & Notification Settings"


class Experience(models.Model):
    ROLE_TYPES = [
        ("WORK", "Professional & Leadership"),
        ("ACADEMIC", "Academic & Research"),
        ("EDUCATION", "Education & Degree"),
    ]
    role_type = models.CharField(max_length=120, choices=ROLE_TYPES, default="WORK")
    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50, default="Present")
    description_markdown = models.TextField(blank=True, help_text="Supports Markdown.")
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return f"{self.title} - {self.organization}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("AI_NLP", "AI & NLP Research"),
        ("WEB_APP", "Fullstack & PropTech"),
        ("OPEN_SOURCE", "Open Source & Tools"),
    ]
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="WEB_APP", db_index=True)
    summary = models.TextField(max_length=350, help_text="Short card summary.")
    details_markdown = models.TextField(blank=True, help_text="Detailed project write-up in Markdown.")
    tech_stack = models.CharField(max_length=200, help_text="Comma-separated: Python, Django, PyTorch")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def tech_list(self):
        return [tag.strip() for tag in self.tech_stack.split(",") if tag.strip()]

    def __str__(self):
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=255)
    venue = models.CharField(max_length=200)
    year = models.PositiveIntegerField(db_index=True)
    paper_url = models.URLField(blank=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["-year", "title"]

    def __str__(self):
        return f"{self.title} ({self.year})"


class BlogPost(models.Model):
    """Multi-language Markdown blog posts. """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=320, help_text="Short preview summary shown on the homepage and blog list.")
    content_markdown = models.TextField(help_text="Full article written in Markdown.")
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags, e.g. NLP, Python, AI")
    is_published = models.BooleanField(default=True, db_index=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def reading_time_minutes(self):
        words = len((self.content_markdown or "").split())
        return max(1, math.ceil(words / 200))

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=120)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sender_name}: {self.subject}"