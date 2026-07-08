import smtplib

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage

from rdmo.core.exceptions import MailSendError


def _format_smtp_exception(exception):
    if isinstance(exception, smtplib.SMTPRecipientsRefused):
        details = []
        for _recipient, (_code, response) in exception.recipients.items():
            if isinstance(response, bytes):
                response = response.decode(errors='replace')
            details.append(response)
        return '; '.join(details) if details else str(exception)

    if isinstance(exception, smtplib.SMTPResponseException):
        response = exception.smtp_error
        if isinstance(response, bytes):
            response = response.decode(errors='replace')
        return f'{response}' if response else str(exception)

    return str(exception)


def send_mail(subject, message, from_email=None, to=None, cc=None, bcc=None, reply_to=None, attachments=None):
    site = Site.objects.get_current()
    subject = f'[{site.name}] ' + subject

    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    mail = EmailMessage(subject, message, from_email, to=to, cc=cc, bcc=bcc, reply_to=reply_to, attachments=attachments)
    try:
        mail.send()
    except smtplib.SMTPException as e:
        raise MailSendError(_format_smtp_exception(e), original_exception=e) from e
