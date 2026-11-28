from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from decouple import config
from core import views

# Non-prefixed URLs (Language switcher endpoint)
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

# Language-prefixed URLs (/en/, /km/, /fr/)
urlpatterns += i18n_patterns(
    path(config("ADMIN_URL", default="portal-manage/"), admin.site.urls),
    path("", views.home_view, name="home"),
    path("blogs/", views.blog_list_view, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail_view, name="blog_detail"),
    path("hx/projects/", views.filter_projects_hx, name="hx_filter_projects"),
    path("hx/contact/", views.contact_submit_hx, name="hx_contact_submit"),
)

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=[
            path("__debug__/", include("debug_toolbar.urls"))
    ] 