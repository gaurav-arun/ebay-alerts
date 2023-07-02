from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import datetime
from email.mime.base import MIMEBase
from typing import TYPE_CHECKING, Union

import html2text
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# from . import get_dashboard_url
# from .context_processors import settings_constants

if TYPE_CHECKING:
    # from customer.models import User as CustomerUser

    UserOrEmail = str

logger = logging.getLogger(__name__)


def format_user_email(user) -> str:
    """
    Returns the email address if it is a User instance,, otherwise returns the original string

    Important
    ----------
    It also used to format the email string as follows:
    Eg. John Doe <john@example.com>

    See the comment inline as to why we've disabled formatting temporarily.
    TODO: Should we turn it back on after testing?

    Parameters
    ----------
        user: a User instance, or a string email address.
    """
    if isinstance(user, str):
        return user
    return user.email
    # The following no longer works because of the following error:
    # 555 5.5.2 Syntax error. gmail's smtp
    # See https://github.com/elbuo8/sendgrid-django/pull/87
    # We can re-enable after the above gets merged
    # if user.first_name and user.last_name:
    #     formatted_email = f"{user.first_name} {user.last_name} <{user.email}>"
    # else:
    #     formatted_email = f"{user.email}"
    # return formatted_email


def make_unique(
    to: Sequence[str], cc: Sequence[str], bcc: Sequence[str]
) -> tuple[list[str], list[str], list[str]]:
    """
    Remove duplicate/repeating emails across to, cc, bcc.
    """
    to_set = set(to)
    cc_set = set(cc)
    bcc_set = set(bcc)

    cc_set = cc_set.difference(to_set)
    bcc_set = bcc_set.difference(to_set.union(cc_set))

    return list(to_set), list(cc_set), list(bcc_set)


def send_html_mail(
    template_name: str,
    context: dict = None,
    from_email: str = settings.DEFAULT_FROM_EMAIL,
    to: Sequence[UserOrEmail] = None,
    bcc: Sequence[UserOrEmail] = None,
    cc: Sequence[UserOrEmail] = None,
    reply_to: str = None,
    headers: dict[str, str] = None,
    # attachments=None,
):
    """Sends email rendered via templates.

    If `from_email` is a list of user instances or a single one,
    it will build a custom formatting for them using the stored data
    "Full Name <email@example.com>".

    This allows us to keep base email templates and just edit the parts of
    the body or subject.

    Also we're using a single template for all related notifications.
    Both email subject/body are saved in the same template.

    Parameters
    ----------
    template_name: str
        Relative template path. See 'mails/base.html' for the block names to use.
    context: dict
        Dictionary containing values to plug into the template
    from_email: str
        String, containing email address on behalf of whom this email is sent. Provided by default in settings.
    to: list(UserOrEmail)
        a list of email addresses or User instances, for the TO field.
    bcc: list(UserOrEmail)
        a list of email addresses, for the BCC field
    cc: list(UserOrEmail)
        a list of email addresses, for the CC field headers: Eg. {"Reply-To": "another@example.com"}
    attachments: list(dict)
        List of Dictionary objects with the following format.
        [{"name": "test.txt", "file_path": company_869445/kyc_documents/form_T9lIHIz.txt }], where file_path is
        relative path of file. Since our files are stored on S3 we have to read the contents in the task using the
        default storage class(Boto in our case).
    """

    # Set default recipient values
    to = to or []
    cc = cc or []
    bcc = bcc or []

    # This safeguard is done till we figure out how *not* to match type hint
    # List[str] versus str
    if isinstance(to, str):
        to = [to]
    if isinstance(cc, str):
        cc = [cc]
    if isinstance(bcc, str):
        bcc = [bcc]

    # # TODO: turn this off here and turn on bcc for all emails via sendgrid instead
    # if settings.AIRBASE_BCC_EMAIL and isinstance(bcc, list):
    #     bcc.append(settings.AIRBASE_BCC_EMAIL)

    # Replace with email addresses + format if User instances
    formatted_to = [format_user_email(item) for item in to]
    formatted_cc = [format_user_email(item) for item in cc]
    formatted_bcc = [format_user_email(item) for item in bcc]
    unique_to, unique_cc, unique_bcc = make_unique(
        formatted_to, formatted_cc, formatted_bcc
    )

    # headers = headers or {}
    # if reply_to:
    #     headers["Reply-To"] = reply_to

    # context = context or {}
    # context.update(**settings_constants())
    # context.update({"dashboard_url": get_dashboard_url()})
    # context["year"] = datetime.today().year

    # Rendering subject
    context["render_subject"] = True
    subject = render_to_string(template_name, context)
    subject = subject.replace("\r", " ").replace("\n", " ").strip()
    subject = "".join(subject.splitlines())
    # if settings.AIRBASE_ENVIRONMENT != "production":
    #     subject = f"[{settings.AIRBASE_ENVIRONMENT.upper()}] {subject}"

    # Rendering body(both html + text version)
    context["render_subject"] = False
    html_version = render_to_string(template_name, context).strip()
    text_version = html2text.html2text(html_version)

    # Create message from subject, html, and text version
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_version,
        from_email=from_email,
        to=unique_to,
        cc=unique_cc,
        bcc=unique_bcc,
        headers=headers,
    )
    message.attach_alternative(html_version, "text/html")

    # Attach files
    # attachments = attachments or []
    # for attachment in attachments:
    #     name = attachment["name"]
    #     file_content = attachment.get("file_content")
    #     if file_content:
    #         message.attach(name, file_content)
    #     else:
    #         file_path = attachment["file_path"]
    #         docfile = default_storage.open(file_path, "rb")
    #         if docfile:
    #             part = MIMEBase("application", "octet-stream")
    #             part.set_payload(docfile.read())
    #             part.add_header("Content-Disposition", f'attachment; filename="{name}"')
    #             message.attach(part)

    # Adds template_name as category for sendgrid,
    # so we can group stats by category
    # message.categories = [template_name]

    # message.send() returns AsyncResult instances for async email tasks triggered by `djcelery_email` lib. On prod,
    # we currently use `anymail.backends.sendgrid.EmailBackend` service which performs the `send-mail` SendGrid API
    # call to pass the email message from our BE to SendGrid.
    return message.send()
