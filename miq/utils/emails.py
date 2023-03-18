from django.template import render_to_string
from django.core.mail import EmailMessage


def send_email_with_attachment(
        subject, message, from_email, recipient_list, fail_silently=False,
        auth_user=None, auth_password=None, connection=None, html_message=None,
        attachments=None):
    """
    Sends an email to the recipient_list.
    """

    mail = EmailMessage(subject, message, from_email, recipient_list, connection=connection)
    mail.attach(attachments)
    mail.send(
        html_message=html_message, fail_silently=fail_silently,
        auth_user=auth_user, auth_password=auth_password,
    )


def send_email(subject: str, message: str, from_email, recipient_list, html_message=None, **kwargs):

    # auth_user=None, auth_password=None, connection=None, html_message=None
    """
    Sends an email to the recipient_list.
    """

    mail = EmailMessage(subject, message, from_email, recipient_list, connection=kwargs.get('connection'))

    if html_message:
        mail.content_subtype = "html"

    mail.send(
        html_message=html_message, fail_silently=kwargs.get('fail_silently', False),
        auth_user=kwargs.get('auth_user'), auth_password=kwargs.get('auth_password'),
    )


def send_email_template(
        subject, template, context, from_email, recipient_list, fail_silently=False,
        auth_user=None, auth_password=None, connection=None, html_message=None):
    """
    Sends an email to the recipient_list.
    """
    message = render_to_string(template, context)
    send_email(subject, message, from_email, recipient_list, fail_silently,
               auth_user, auth_password, connection, html_message)
