import json
import logging
import threading
import urllib.request
from django.conf import settings
from django.core.mail import send_mail
from .models import SiteProfile

logger = logging.getLogger(__name__)


def _send_telegram_message(contact_msg):
    """Send a formatted message to your telegram via the official Bot HTTP API."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        logger.warning("Telegram credentials missing in .env; skipping Telegram alert.")
        return

    text = (
        f"*New porfolio message*\n\n"
        f"*From:* {contact_msg.sender_name} ({contact_msg.sender_email})\n"
        f"*Subject:* {contact_msg.subject}\n\n"
        f"*Message:*\n{contact_msg.message}"
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    playload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }).encode("utf-8")

    req = urllib.request.Request(url, data=playload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            response.read()
    except Exception as exc:
        logger.error("Fail to send Telegram notification")


def _send_email_notification(contact_msg):
    """Send an email alert via Django's configured SMTP server."""
    receiver = settings.NOTIFICATION_RECEIVER_EMAIL
    if not settings.EMAIL_HOST_USER or not receiver:
        logger.warning("Email credentials missing in .env; skipping Email alert.")
        return

    subject = f"[Portfolio Contact] {contact_msg.subject}"
    body = (
        f"You received a new message from  your portfolio website:\n\n"
        f"Name: {contact_msg.sender_name}\n"
        f"Email: {contact_msg.sender_email}\n"
        f"Subject: {contact_msg.subject}\n\n"
        f"Message:\n{contact_msg.message}"
    )
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[receiver],
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Failed to send email notification: %s", exc)


def dispatch_contact_notifications(contact_msg):
    """
    checks your live Admin CMS toggles and runs enabled notifications asynchronously.
    """
    profile = SiteProfile.objects.first()
    send_tg = profile.enable_telegram_alerts if profile else True
    send_em = profile.enable_email_alerts if profile else True

    def _worker():
        if send_tg:
            _send_telegram_message(contact_msg)
        if send_em:
            _send_email_notification(contact_msg)

    threading.Thread(target=_worker, daemon=True).start()