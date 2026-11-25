# portfolio-2.0

A dynamic, multilingual (`English`, `ខ្មែរ`, `Français`), database-driven personal portfolio and academic/engineering CMS built with **Python (Django 5)**, **HTMX**, and **Tailwind CSS**.

Every section—including biography, downloadable CV, career experience, featured projects, academic publications, and Markdown blog articles—is managed dynamically through a custom Admin CMS without modifying source code.

---

## Core Features

- **100% Dynamic Admin CMS:** Powered by `django-unfold` with tabbed multi-language fields (`django-modeltranslation`).
- **Seamless Multilingual Support (`i18n`):** Instant horizontal language switcher supporting **English (`en`)**, **Khmer (`km`)**, and **French (`fr`)** with SEO-friendly URL prefixes (`/en/`, `/km/`, `/fr/`). Easily extensible to additional languages via `config/settings.py`.
- **Full Markdown Publishing Engine:** Write rich biographies, project write-ups, and blog articles in Markdown with automatic reading-time calculation and syntax-highlighted code blocks.
- **Adaptive Light & Dark Theme:** System-aware theme detection with a persistent manual Light/Dark mode toggle (`localStorage`) styled in **Google Sans**.
- **Asynchronous Contact Alerts:** HTMX-powered contact form that saves inquiries to the database and dispatches real-time **Telegram Bot** and **Email (SMTP)** alerts in background threads—each toggleable directly from the Admin dashboard.

---

## Tech Stack

- **Backend:** Python 3.11+, Django 5
- **Frontend Interactivity & Styling:** HTMX 1.9, Tailwind CSS (Typography + Class Dark Mode), Google Sans
- **Internationalization:** Django `i18n` + `django-modeltranslation`
- **Admin UI:** `django-unfold`
- **Database:** SQLite (Local Development) / PostgreSQL (Production)
- **Production Edge & Hosting:** Docker + Gunicorn + Nginx behind Cloudflare Reverse Proxy & WAF

---

## Project Structure

```text
portfolio-2.0/
├── config/                 # Project settings, root URLs, WSGI/ASGI entrypoints
│   ├── settings.py         # Core configuration, LANGUAGES list, SMTP & Telegram env hooks
│   └── urls.py             # i18n URL routing (/en/, /km/, /fr/)
├── core/                   # Main portfolio & blog application
│   ├── models.py           # SiteProfile, Experience, Project, Publication, BlogPost, ContactMessage
│   ├── translation.py      # Registers model fields for multi-language database columns
│   ├── admin.py            # Tabbed multi-language Admin CMS configuration
│   ├── views.py            # Homepage, Blog archive/detail, and HTMX endpoints
│   ├── notifications.py    # Background Telegram & Email alert dispatcher
│   └── templatetags/       # Custom Markdown rendering filter (render_markdown)
├── templates/              # Responsive HTML templates
│   ├── base.html           # Master layout (Navbar, Language Pills, Theme Toggle, Footer)
│   ├── home.html           # Main portfolio landing page
│   ├── blog_list.html      # Published blog archive
│   ├── blog_detail.html    # Full blog article reader
│   └── partials/           # HTMX dynamic HTML fragments
├── locale/                 # Compiled .po/.mo static UI translation files
├── media/                  # User-uploaded avatars, CVs, and blog cover images
├── .env                    # Environment secrets (ignored by Git)
└── manage.py               # Django management CLI