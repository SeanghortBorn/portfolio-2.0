# portfolio-2.0 — Golden Architecture & A-to-Z Engineering Guide

**Project Name:** `portfolio-2.0`  
**Owner:** Seanghort Born  
**Observed local environment:** Python 3.14.4 and Django 6.1.3. No dependency manifest is present, so the supported Python/Django version range is not declared.  
**Stack:** Django, HTMX, Tailwind CSS (CDN), Google Sans, `django-modeltranslation`, `django-unfold`  
**Purpose:** Single source of truth covering system architecture, data models, internationalization (`i18n`), Markdown rendering, asynchronous Telegram/Email notifications, Light/Dark UI theming, local development, troubleshooting, and production deployment.

---

## Table of Contents

1. [System Vision & Architectural Overview](#1-system-vision--architectural-overview)
2. [Non-Functional Requirements (NFR) & Security](#2-non-functional-requirements-nfr--security)
3. [Directory & File Map](#3-directory--file-map)
4. [Environment Configuration (`.env` & `config/settings.py`)](#4-environment-configuration-env--configsettingspy)
5. [Database Schema & Models (`core/models.py`)](#5-database-schema--models-coremodelspy)
6. [Multi-Language System (`i18n` + `django-modeltranslation`)](#6-multi-language-system-i18n--django-modeltranslation)
7. [Admin CMS (`core/admin.py`)](#7-admin-cms-coreadminpy)
8. [Markdown Engine, Views, URLs & HTMX](#8-markdown-engine-views-urls--htmx)
9. [Notification Dispatcher (Telegram & Email)](#9-notification-dispatcher-telegram--email)
10. [Frontend Architecture: Google Sans, Language Pills, Light/Dark Mode & Footer](#10-frontend-architecture-google-sans-language-pills-lightdark-mode--footer)
11. [Day-to-Day Workflows: Adding Languages, Content & Backups](#11-day-to-day-workflows-adding-languages-content--backups)
12. [Local Development & Troubleshooting Playbook](#12-local-development--troubleshooting-playbook)
13. [Production Deployment (VPS + Docker + Cloudflare Edge)](#13-production-deployment-vps--docker--cloudflare-edge)

---

## 1. System Vision & Architectural Overview

`portfolio-2.0` is a **database-driven fullstack web application and CMS** built on Django's **MVT (Model-View-Template)** architecture, enhanced with **HTMX** for partial page updates without heavy JavaScript frameworks.

### Request Lifecycle

1. **Client Request:** A visitor visits `/en/`, `/km/`, or `/fr/` (or clicks a language pill / HTMX filter / contact form).
2. **Middleware Chain (`config/settings.py`):**
   - `SecurityMiddleware` & `WhiteNoiseMiddleware` handle security headers and static assets.
   - `SessionMiddleware` & `LocaleMiddleware` resolve the active language from the URL prefix, session, or cookie.
   - `CsrfViewMiddleware` & `AuthenticationMiddleware` protect forms and power the Admin CMS.
3. **URL Routing (`config/urls.py`):**
   - `/i18n/` handles Django's `set_language` POST endpoint.
   - `i18n_patterns` routes language-prefixed paths (`<ADMIN_URL>`, `/`, `/blogs/`, `/blog/<slug>/`, `/hx/projects`, `/hx/contact/`).
4. **View Layer (`core/views.py`):**
   - Queries Django ORM models (`SiteProfile`, `Experience`, `Project`, `Publication`, `BlogPost`) filtered for the active language.
   - For HTMX endpoints (`filter_projects_hx`, `contact_submit_hx`), returns only HTML fragments (`templates/partials/*.html`) rather than full pages.
5. **Template & Rendering Layer (`templates/*.html`):**
   - Renders Google Sans typography, Light/Dark theme classes, `{% trans %}` UI strings, and `|render_markdown` HTML output.

---

## 2. Non-Functional Requirements (NFR) & Security

| Requirement | Implementation in `portfolio-2.0` |
| :--- | :--- |
| **User-Friendly CMS** | `django-unfold` provides a modern dashboard; `TabbedTranslationAdmin` organizes per-language fields into tabs; `list_editable` enables quick visibility and ordering toggles. |
| **Modern UI/UX** | Tailwind CSS with `darkMode: 'class'`, HTMX live project filtering and contact submission, and rounded UI components (`rounded-2xl` / `rounded-full`). |
| **Security** | Django ORM parameterized queries prevent SQL injection; template auto-escaping applies to ordinary output, but Markdown is marked safe and is not sanitized; CSRF tokens protect POST forms; Admin path is configurable via `ADMIN_URL`. |
| **Flexibility** | `SiteProfile` acts as a singleton for global profile info and notification flags; adding/removing languages is driven by `LANGUAGES` in `config/settings.py`. |
| **Responsiveness** | Mobile-first Tailwind grid breakpoints (`sm`, `md`, `lg`) and dedicated Khmer line-height styling (`:lang(km)`). |
| **Scalability & Maintainability** | Modular `core` app, background threads (`threading.Thread`) for outbound Telegram/Email calls, SQLite locally with straightforward migration to PostgreSQL in production, and JSON backups via `dumpdata`. |

### Security Hygiene Checklist
- Never commit `.env`, `db.sqlite3`, or `media/` to version control. The current checkout has no root `.gitignore`, and `.env` is untracked; add ignore rules before staging files.
- Use a strong, unique `SECRET_KEY` in production and set `DEBUG=False`.
- Keep `ADMIN_URL` non-obvious (for example, `portal-manage/` rather than `admin/`).

---

## 3. Directory & File Map

```text
portfolio-2.0/
├── config/
│   ├── __init__.py
│   ├── settings.py                 # Central settings, LANGUAGES, SMTP & Telegram config
│   ├── urls.py                     # Root & i18n URL patterns
│   ├── wsgi.py                     # WSGI entry point for Gunicorn / servers
│   └── asgi.py                     # ASGI entry point
├── core/
│   ├── __init__.py
│   ├── admin.py                    # Admin CMS registrations & Unfold + TabbedTranslationAdmin
│   ├── apps.py                     # AppConfig for 'core'
│   ├── forms.py                    # ContactForm (ModelForm for ContactMessage)
│   ├── models.py                   # SiteProfile, Experience, Project, Publication, BlogPost, ContactMessage
│   ├── notifications.py            # Toggleable Telegram Bot & SMTP Email sender (threaded)
│   ├── translation.py              # modeltranslation registration for translatable model fields
│   ├── views.py                    # home_view, blog_list_view, blog_detail_view, HTMX views
│   ├── migrations/                 # Auto-generated schema migration files
│   └── templatetags/
│       ├── __init__.py
│       └── markdown_extras.py        # Custom `render_markdown` template filter
├── templates/
│   ├── base.html                   # Shared shell: Google Sans, fixed language pills, theme toggle, footer
│   ├── home.html                   # Hero, About, Projects, Latest Blogs, Publications, Experience, Contact
│   ├── blog_list.html              # Full published blog archive
│   ├── blog_detail.html            # Individual blog post reader
│   └── partials/
│       ├── project_list.html         # Project cards grid (used on load & HTMX filter)
│       └── contact_success.html      # HTMX submission confirmation message
├── locale/                         # Static UI translation catalogs (.po / .mo) per language
├── documents/
│   └── portfolio_2_0_golden_architecture_maintenance_guide.md
├── README.md
├── .env                            # Local environment variables (currently untracked)
├── db.sqlite3                      # Local SQLite database (currently untracked)
├── manage.py                       # Django CLI entry point
└── tem.py                          # Separate file; Django loads templates from templates/
```

`media/` and `staticfiles/` are runtime/upload and collected-static directories; they may not exist in a fresh checkout. The current checkout has no root dependency manifest, Docker Compose file, or Nginx configuration.

---

## 4. Environment Configuration (`.env` & `config/settings.py`)

### `.env` Template

```ini
SECRET_KEY=replace-with-a-long-random-50-character-string
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
ADMIN_URL=portal-manage/

# Email (SMTP) Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
NOTIFICATION_RECEIVER_EMAIL=your-email@example.com

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

### Critical `config/settings.py` Rules
- **App Order:** `unfold` and `modeltranslation` must appear in `INSTALLED_APPS` **before** `django.contrib.admin`.
- **Middleware Order:** `LocaleMiddleware` must appear **after** `SessionMiddleware` and **before** `CommonMiddleware`.
- **Context Processors:** `django.template.context_processors.i18n` must be enabled in `TEMPLATES`.
- **Languages:**
  ```python
  LANGUAGE_CODE = "en"
  USE_I18N = True
  USE_TZ = True

  LANGUAGES = [
      ("en", _("English")),
      ("km", _("ភាសាខ្មែរ")),
      ("fr", _("Français")),
  ]

  MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
  LOCALE_PATHS = [BASE_DIR / "locale"]
  ```
  **Current discrepancy:** `config/settings.py` assigns `LANGUAGES_CODE = "en"` instead of Django's `LANGUAGE_CODE`. `LANGUAGES_CODE` is not Django's language setting; correct it in code before relying on this example.
- **Reverse Proxy Trust:** Include `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` when sitting behind Nginx or Cloudflare HTTPS termination.

---

## 5. Database Schema & Models (`core/models.py`)

| Model | Purpose | Key Fields & Behavior |
| :--- | :--- | :--- |
| `SiteProfile` | Singleton profile & alert toggles | `full_name`, `headline`, `short_bio`, `about_markdown`, `location`, `avatar`, `resume_pdf`, `github_url`, `orcid_url`, `linkedin_url`, `enable_telegram_alerts`, `enable_email_alerts`. `save()` prevents creating more than one row. |
| `Experience` | Career, research & education timeline | `role_type` (`WORK`, `ACADEMIC`, `EDUCATION`), `title`, `organization`, `location`, `start_date`, `end_date`, `description_markdown`, `order`, `is_visible`. Ordered by `["order", "-id"]`. |
| `Project` | Featured work & research projects | `title`, `slug` (unique), `category` (`AI_NLP`, `WEB_APP`, `OPEN_SOURCE`, indexed), `summary`, `details_markdown`, `tech_stack`, `live_url`, `github_url`, `is_featured`, `order`, `created_at`. Includes `tech_list()`. |
| `Publication` | Academic papers & venues | `title`, `authors`, `venue`, `year` (indexed), `paper_url`, `is_visible`. Ordered by `["-year", "title"]`. |
| `BlogPost` | Markdown articles & insights | `title`, `slug` (unique), `excerpt`, `content_markdown`, `cover_image`, `tags`, `is_published` (indexed), `published_at`, `updated_at`. Includes `tag_list()` and `reading_time_minutes()`. |
| `ContactMessage` | Visitor contact submissions | `sender_name`, `sender_email`, `subject`, `message`, `is_read`, `created_at`. Ordered by `["-created_at"]`. |

---

## 6. Multi-Language System (`i18n` + `django-modeltranslation`)

`portfolio-2.0` separates **database content translations** from **static template label translations**:

1. **Dynamic Content (`django-modeltranslation`):**
   - Intended to be registered in `core/translation.py` for `SiteProfile`, `Experience`, `Project`, `Publication`, and `BlogPost`.
   - Generates per-language columns in the database (e.g., `title_en`, `title_km`, `title_fr`).
   - When a visitor browses `/km/`, Django activates `"km"` and automatically reads the `_km` fields (falling back to the default language if a field is left blank).
   - **Current discrepancy:** `BlogPostTranslationOptions` uses `field` rather than `fields` and spells `excerpt` as `excerp`. The existing BlogPost migration has no translated columns, so BlogPost translation is not currently configured as described.
2. **Static UI Labels (Django `i18n`):**
   - Strings in templates wrapped in `{% trans "..." %}` are extracted with `django-admin makemessages -l km -l fr` into `locale/<lang>/LC_MESSAGES/django.po` and compiled into `.mo` files with `django-admin compilemessages`.
3. **URL Prefixing (`i18n_patterns`):**
   - Routes under `i18n_patterns` in `config/urls.py` automatically get language prefixes (`/en/`, `/km/`, `/fr/`).

---

## 7. Admin CMS (`core/admin.py`)

- Uses `unfold.admin.ModelAdmin` combined with `modeltranslation.admin.TabbedTranslationAdmin` on translated models so each language appears in clean tabs inside the edit form.
- Uses `prepopulated_fields = {"slug": ("title",)}` on `Project` and `BlogPost` to generate URL slugs automatically.
- Uses `list_editable` on `SiteProfile` (`enable_telegram_alerts`, `enable_email_alerts`), `Experience` (`order`, `is_visible`), `Project` (`is_featured`, `order`), `Publication` (`is_visible`), `BlogPost` (`is_published`), and `ContactMessage` (`is_read`) for rapid updates from list views.
- Marks `ContactMessage` content fields as `readonly_fields` so incoming visitor messages are preserved unaltered.

---

## 8. Markdown Engine, Views, URLs & HTMX

### Markdown Rendering (`core/templatetags/markdown_extras.py`)
- Registers the `render_markdown` filter using Python's `markdown` library and returns `mark_safe(html)`.
- Used on `profile.about_markdown`, `project.details_markdown`, `item.description_markdown`, and `post.content_markdown`.
- **Current discrepancy:** The configured extensions include `"sane_list"`, which is not an installed Markdown extension name in the current environment; rendering Markdown raises `ModuleNotFoundError`. This was verified by invoking the configured extension list. The earlier `"sane_lists"` spelling in this guide also did not match the code.
- Because the filter marks generated HTML safe, Django template auto-escaping does not sanitize raw HTML included in Markdown.

### Views (`core/views.py`) & Routes (`config/urls.py`)
- `home_view` (`/` inside `i18n_patterns`): Fetches `SiteProfile`, visible `Experience`, featured `Project` items, visible `Publication` items, top 3 published `BlogPost` items (`[:3]`), `categories`, a blank `ContactForm`, and `current_year`.
- `blog_list_view` (`/blogs/`): Lists all published `BlogPost` entries.
- `blog_detail_view` (`/blog/<slug:slug>/`): Renders a single published `BlogPost` or returns `404`.
- `filter_projects_hx` (`/hx/projects`): Intended to read `?category=...` (`ALL` or a category code) and return `templates/partials/project_list.html` for HTMX target replacement. **Current discrepancy:** The non-`ALL` branch does not filter by category and assigns a one-element tuple instead of a queryset, so category filtering is currently broken.
- `contact_submit_hx` (`/hx/contact/`, `@require_POST`): Validates `ContactForm`; on valid input, saves `ContactMessage`, triggers `dispatch_contact_notifications(msg)`, and returns `templates/partials/contact_success.html`.
- **Current discrepancy:** On invalid input, the view references `templates/partials/contact_form.html`, but that template is absent from the current checkout.

---

## 9. Notification Dispatcher (Telegram & Email)

Located in `core/notifications.py`:

- `dispatch_contact_notifications(contact_msg)` reads the `SiteProfile` singleton (`enable_telegram_alerts` and `enable_email_alerts`), defaulting to `True` if no profile exists yet.
- Spawns a daemon `threading.Thread` so external network calls (Telegram Bot API HTTP POST and SMTP email) do not block or slow down the visitor's HTTP/HTMX response.
- **Telegram (`_send_telegram_message`):** Posts Markdown-formatted message details to `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendMessage` for `TELEGRAM_CHAT_ID` with a 5-second timeout.
- **Email (`_send_email_notification`):** Sends via Django's `send_mail` using `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `NOTIFICATION_RECEIVER_EMAIL`.
- Both helpers log warnings/errors via Python's `logging` module if credentials are missing or a network call fails.

---

## 10. Frontend Architecture: Google Sans, Language Pills, Light/Dark Mode & Footer

### Typography (`Google Sans`)
- `templates/base.html` loads `Google Sans` from Google Fonts and applies it across `body, button, input, textarea, select` so English, Khmer (`ខ្មែរ`), and French (`Français`) share consistent typography, with extra line-height (`line-height: 1.85`) on `:lang(km)`.

### Fixed Horizontal Language Switcher
- Inside `templates/base.html`, a `<form action="{% url 'set_language' %}" method="post">` renders three pill buttons (`ខ្មែរ` -> `km`, `English` -> `en`, `Français` -> `fr`) in a fixed horizontal bar regardless of the active language, highlighting the current language (`CURRENT_LANG`) with `#E61D4E`.

### Light & Dark Mode
- Tailwind CSS is configured with `darkMode: 'class'`.
- An inline `<script>` in `<head>` checks `localStorage.getItem('theme')` and `window.matchMedia('(prefers-color-scheme: dark)')` before first paint to avoid a theme flash.
- Clicking `#theme-toggle` toggles `.dark` on `document.documentElement` and saves `'dark'` or `'light'` to `localStorage`.

### Footer & Spacing Controls
- `templates/base.html` includes a footer with brand info, navigation links (`About`, `Experience`, `Projects`, `Publications`, `Blogs`, `Contact`), dynamic `{{ current_year }}` copyright notice, and social links.
- Current footer spacing uses `py-8` on the container, `pb-8` on the upper row, `pt-6` on the copyright row, and `mt-8` on `<footer>`.
- Corner roundness across components is controlled via Tailwind radius classes (`rounded-full` for pills/badges/toggles, `rounded-2xl` or `rounded-3xl` for cards, inputs, buttons, and images).

---

## 11. Day-to-Day Workflows: Adding Languages, Content & Backups

### Adding or Removing a Language
1. Update `LANGUAGES` in `config/settings.py` (e.g., add `("ja", _("日本語"))` or remove an entry).
2. Run migrations so database columns are created/updated:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Generate and compile static UI strings for any new language code:
   ```bash
   django-admin makemessages -l <lang_code>
   django-admin compilemessages
   ```
4. Update the horizontal language pill buttons in `templates/base.html` if you want the new language button shown in the navbar pill bar.

### Publishing Content
1. Start the server (`python manage.py runserver`) and open `/<lang>/<ADMIN_URL>/` (e.g., `http://127.0.0.1:8000/en/portal-manage/`).
2. Edit `SiteProfile` (including `enable_telegram_alerts` and `enable_email_alerts`), or create/edit `Project`, `Publication`, `Experience`, or `BlogPost` entries across the language tabs.
3. Verify on `/en/`, `/km/`, and `/fr/`.

### Backing Up & Restoring Data
- **Export backup:**
  ```bash
  python manage.py dumpdata core --indent 2 > backup_core.json
  ```
- **Restore backup into a fresh database (after `migrate`):**
  ```bash
  python manage.py loaddata backup_core.json
  ```

---

## 12. Local Development & Troubleshooting Playbook

### Standard Local Startup
```bash
cd ~/Projects/portfolio-2.0
source .venv/bin/activate
python manage.py migrate
django-admin compilemessages
python manage.py runserver
```

Run `python manage.py makemigrations` only after changing models; inspect and keep the generated migration, then apply it with `python manage.py migrate`. The repository currently has no dependency manifest, so these steps assume the environment has already been provisioned.

### Common Issues & Fixes
- **Cannot log into Admin CMS / Forgot password:**
  ```bash
  python manage.py changepassword <username>
  ```
  To check existing superuser usernames:
  ```bash
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(list(User.objects.filter(is_superuser=True).values_list('username', 'email')))"
  ```
- **Login page reloads without error locally:** Ensure `DEBUG=True` in `.env` when running over `http://127.0.0.1:8000` without HTTPS.
- **`makemessages` / `compilemessages` fails:** Install GNU `gettext` on your OS (e.g., `sudo apt install gettext` on Ubuntu/Debian).
- **Model or translation changes not reflected in DB:** Always run both `python manage.py makemigrations` and `python manage.py migrate`.

---

## 13. Production Deployment (VPS + Docker + Cloudflare Edge)

The following is a **proposed deployment topology**, not configuration present in the current checkout. The project settings currently use SQLite directly; no Docker Compose, Nginx, PostgreSQL, or `DATABASE_URL` configuration is present.

1. **Application & Database on VPS:**
   - Run Django via **Gunicorn** alongside **PostgreSQL** (`psycopg[binary]` + `dj-database-url`) and **Nginx** inside Docker Compose.
   - Set `DEBUG=False`, configure a strong `SECRET_KEY`, set `ALLOWED_HOSTS` to your production domain(s), and run `python manage.py collectstatic` for `WhiteNoise`.
2. **Cloudflare DNS, SSL & WAF:**
   - Point DNS `A`/`AAAA` records to your VPS IP with **Proxied (Orange Cloud)** enabled so Cloudflare hides your origin IP and filters malicious traffic.
   - Use **SSL/TLS: Full (Strict)** with a Cloudflare Origin Certificate on Nginx.
3. **Edge Caching & Firewall:**
   - Add a Cloudflare Cache Rule for `/static/*` and `/media/*` to improve global load times.
   - Restrict VPS HTTP/HTTPS (`80`/`443`) firewall rules (e.g., `ufw`) to Cloudflare IP ranges while keeping SSH (`22`) restricted to your management IP/key.