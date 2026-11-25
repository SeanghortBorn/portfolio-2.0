from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import SiteProfile, Experience, Project, Publication, BlogPost
from .forms import ContactForm
from .notifications import dispatch_contact_notifications


def home_view(request):
    """Main portfolio view. Automatically serves the active language (en, km, or fr)."""
    profile = SiteProfile.objects.first()
    experiences = Experience.objects.filter(is_visible=True)
    projects = Project.objects.filter(is_featured=True)
    publications = Publication.objects.filter(is_visible=True)
    recent_blogs = BlogPost.objects.filter(is_published=True)[:3]

    context = {
        "profile": profile,
        "experiences": experiences,
        "projects": projects,
        "publications": publications,
        "recent_blogs": recent_blogs,
        "categories": Project.CATEGORY_CHOICES,
        "contact_form": ContactForm(),
        "current_year": datetime.now().year,
    }
    return render(request, "home.html", context)


def blog_list_view(request):
    """Full archived of published blog posts."""
    profile = SiteProfile.objects.first()
    blogs = BlogPost.objects.filter(is_published=True)
    return render(request, "blog_list.html", {
        "profile": profile,
        "blogs": blogs,
        "current_year": datetime.now().year,
    })


def blog_detail_view(request, slug):
    """Individual blog article reader view."""
    profile = SiteProfile.objects.first()
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, "blog_detail.html", {
        "profile": profile,
        "post": post,
        "current_year": datetime.now().year,
    })


def filter_projects_hx(request):
    category = request.GET.get("category", "ALL")
    if category == "ALL" or not category:
        projects = Project.objects.filter(is_featured=True)
    else:
        projects = Project.objects.filter(is_featured=True),
    return render(request, "partials/project_list.html", {"projects": projects})


@require_POST
def contact_submit_hx(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        msg = form.save()
        # Trigger Telegram and or Email notifications based on Admin toggles
        dispatch_contact_notifications(msg)
        return render(request, "partials/contact_success.html")
    return render(request, "partials/contact_form.html", {"contact_form": form})