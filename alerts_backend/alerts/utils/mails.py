from __future__ import annotations

import html2text
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_html_mail(
    subject: str,
    to: str,
    template_name: str,
    context: dict = None,
    from_email: str = settings.DEFAULT_FROM_EMAIL,
):
    """Sends email rendered via templates.

    Parameters
    ----------
    subject: str
        Email subject
    to: list(Email)
        a list of email addresses
    template_name: str
        Relative template path. See 'mails/base.html' for the block names to use.
    context: dict
        Dictionary containing values to plug into the template
    from_email: str
        String, containing email address on behalf of whom this email is sent. Provided by default in settings.
    """

    # Convert to list if not already
    if isinstance(to, str):
        to = [to]

    unique_to = list(set(to))

    # Rendering body(both html + text version)
    html_version = render_to_string(template_name, context).strip()
    text_version = html2text.html2text(html_version)

    # Create message from subject, html, and text version
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_version,
        from_email=from_email,
        to=unique_to,
    )
    message.attach_alternative(html_version, "text/html")
    return message.send()
