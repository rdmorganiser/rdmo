import smtplib

import pytest

from django.conf import settings
from django.core import mail

from rdmo.core.exceptions import SendMailException
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


@pytest.mark.parametrize('mail_exception', [
    pytest.param(
        smtplib.SMTPRecipientsRefused({
            'name@non-existent-domain.abc': (550, b'Domain not found')
        }),
        id='recipient-refused'
    ),
    pytest.param(ConnectionRefusedError('Connection refused'), id='connection-refused')
])
def test_send_mail_error(db, mocker, mail_exception):
    mocker.patch(
        'rdmo.core.mail.EmailMessage.send',
        side_effect=mail_exception
    )

    with pytest.raises(SendMailException) as e:
        send_mail('Subject', 'Message', to=['user@example.com'])

    assert str(e.value) == str(mail_exception)
