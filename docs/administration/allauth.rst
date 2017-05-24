Social accounts
---------------

If you use allauth as you mode of authentication and configured RDMO to use one or more OAUTH provider (as described in the :doc:`Configuration chapter </configuration/authentication/allauth>`), you need to register your RDMO site with theses services. This process is different from provider to provider. Usually, you need to provide a set of information about your site. Always included is a redirect or callback url. In the following we will use http://127.0.0.1:8000 as an example (which will work on the development server) and you will need to replace that with the correct url of your RDMO application in production.

ORCID
    Login into https://orcid.org and go to the developer tools page at https://orcid.org/developer-tools. Create an app with the Redirect URI

    ::

        http://127.0.0.1:8000/account/orcid/login/callback/

github
    Login into github and go to https://github.com/settings/applications/new and create a new app. Use

    ::

        http://127.0.0.1:8000/account/github/login/callback/

facebook
    Login into facebook and go to https://developers.facebook.com/. Click on the top right menu *My Apps* and choose *Add a new app*. Create a new app. In the following screen choose Facebook login -> Getting started and choose *Web* as the platform. Put in a URL under which your application is accessible (Note: 127.0.0.1 will not work here.). Back on the dashboard, go to Settings -> Basic and copy the `App ID` and the `App Secret`.


twitter
    Login into twitter and go to https://apps.twitter.com/app/new and create a new app. Use

    ::

        http://127.0.0.1:8000/account/facebook/login/callback/

    as the Authorized redirect URI. Copy the Client-ID and the Client key.

Google
    Login into google and go to https://console.developers.google.com. Create a new project. After the project is created go to Credentials on the left side and configure the OAuth Authorization screen (second tab). Then create the credentials (first tab), more precisely a OAuth Client-ID. Use

    ::

        http://127.0.0.1:8000/account/google/login/callback/

    as the Authorized redirect URI. Copy the Client-ID and the Client key.

Once the credentials are obtained you need to enter them in the admin interface. To this purpose, go to **Social applications** under **SOCIAL ACCOUNTS** and click on **Add social application**. Then:

1. Select the corresponding **provider**

2. Enter a **Name** of your choice

3. Enter the **Client id** (or App ID) and the **Secret key** (or Client secret, Client key, App Secret)

4. Add your site to the chosen sites.

5. Click save.
