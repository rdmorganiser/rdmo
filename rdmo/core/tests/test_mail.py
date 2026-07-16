import smtplib

import pytest

from django.conf import settings
from django.core import mail

from rdmo.core.exceptions import MailSendError
from rdmo.core.mail import send_mail


def test_send_mail(db):
    send_mail('Subject', 'Message', to=['user@example.com'])

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[example.com] Subject'
    assert mail.outbox[0].body == 'Message'
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].to == ['user@example.com']
    assert mail.outbox[0].cc == []
    assert mail.outbox[0].bcc == []
    assert mail.outbox[0].attachments == []


def test_send_mail_cc(db):
    send_mail('Subject', 'Message', to=['user@example.com'], cc=['user2@example.com'])

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[example.com] Subject'
    assert mail.outbox[0].body == 'Message'
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].to == ['user@example.com']
    assert mail.outbox[0].cc == ['user2@example.com']
    assert mail.outbox[0].bcc == []
    assert mail.outbox[0].attachments == []


def test_send_mail_bcc(db):
    send_mail('Subject', 'Message', bcc=['user2@example.com'])

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[example.com] Subject'
    assert mail.outbox[0].body == 'Message'
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].to == []
    assert mail.outbox[0].cc == []
    assert mail.outbox[0].bcc == ['user2@example.com']
    assert mail.outbox[0].attachments == []


def test_send_mail_from_email(db):
    send_mail('Subject', 'Message', from_email='user@example.com', to=['user2@example.com'])

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[example.com] Subject'
    assert mail.outbox[0].body == 'Message'
    assert mail.outbox[0].from_email == 'user@example.com'
    assert mail.outbox[0].to == ['user2@example.com']
    assert mail.outbox[0].cc == []
    assert mail.outbox[0].bcc == []
    assert mail.outbox[0].attachments == []


def test_send_mail_from_attachments(db):
    send_mail('Subject', 'Message', to=['user2@example.com'], attachments=[
        ('Attachment', b'attachment', 'plain/text')
    ])

    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == '[example.com] Subject'
    assert mail.outbox[0].body == 'Message'
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].to == ['user2@example.com']
    assert mail.outbox[0].cc == []
    assert mail.outbox[0].bcc == []
    assert mail.outbox[0].attachments == [
        ('Attachment', b'attachment', 'plain/text')
    ]


def test_send_mail_recipient_refused(db, mocker):
    smtp_exception = smtplib.SMTPRecipientsRefused({
        'name@non-existent-domain.abc': (
            550,
            b'Domain not found'
        )
    })

    mocker.patch(
        'rdmo.core.mail.EmailMessage.send',
        side_effect=smtp_exception
    )

    with pytest.raises(MailSendError) as e:
        send_mail('Subject', 'Message', to=['name@non-existent-domain.abc'])

    assert e.value.reason == str(smtp_exception)
