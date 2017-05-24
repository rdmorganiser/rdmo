Auth Tokens
-----------

In order to access the data entered into RDMO through the programmable API, a user needs to have a token associated with it. This is done under **AUTH TOKEN / Tokens**. To create a token, click **Add token** on the button at the right and:

1. Select the **user** for the new token.

2. Save the token.

This token can now be used instead of the username and the password when making HTTP requests from a non-browser client. To this purpose, a HTTP-Header of the form

.. code-block:: none

    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

needs to be provided.
