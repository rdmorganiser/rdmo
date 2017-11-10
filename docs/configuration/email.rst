E-Mail
------

RDMO needs to send E-Mails to its users. The connection to the SMPT server is configured several settings in your ``config/settings/local.py``:

.. code:: python

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = '25'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False

    DEFAULT_FROM_EMAIL = ''

Here, ``EMAIL_HOST`` is the URL or IP of the SMTP server, ``EMAIL_PORT`` is the port it is listening on (usually 25, 465, or 587), and  ``EMAIL_HOST_USER`` and ``EMAIL_HOST_PASSWORD`` are credentials if the SMTP server needs authentication.

For a ``STARTTLS`` connection (usually on port 587) ``EMAIL_USE_TLS`` needs to be set to ``True``, while ``EMAIL_USE_SSL`` needs to be set to ``True`` for an implicit TLS/SSL connection (usually on port 465).

``DEFAULT_FROM_EMAIL`` sets the FROM field for the emails send to the users.

For a development/testing setup a simple e-mail backend, which only displays the mail on the terminal can be used:

.. code:: python

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_FROM = 'info@example.com'

This is also the default backend, if no email settings are added to ``config/settings/local.py``.
