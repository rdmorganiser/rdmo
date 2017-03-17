Social apps
~~~~~~~~~~~

Register app
````````````

As the first step register your RDMO application with the particular provider. You need provide a set of information depending on the provider. Always included is a redirect or callback url. In the following we will use http://127.0.0.1:8000 as an example (which will work on the development server) and you will need to replace that with the correct url of your RDMO application in production.

ORCID
    Login into https://orcid.org and go to the developer tools page at https://orcid.org/developer-tools. Create an app with the Redirect URI

    ::

        http://127.0.0.1:8000/account/orcid/login/callback/

github
    Login into github and go to https://github.com/settings/applications/new and create a new app. Use

    ::

        http://127.0.0.1:8000/account/github/login/callback/

facebook
    Login into facebook and go to https://developers.facebook.com/. Click on the top right menu *My Apps* and choose *Add a new app*. Create a new app. In the following screen choose Facebook login -> Getting started and choose *Web* as the platform. Put in URL under which your application is accessible (Note: 127.0.0.1 will not work here.). Back on the dashboard, go to Settings -> Basic and copy the `App ID` and the `App Secret`.


    twitter
    ```````

    Login into twitter and go to https://apps.twitter.com/app/new and create a new app. Use

    ::

        http://127.0.0.1:8000/account/facebook/login/callback/

    as the Authorized redirect URI. Copy the Client-ID and the Client key.

twitter
    Login to twitter and go to https://apps.twitter.com. Click on "Create New App" to create a new app. Use

    ::

        https://127.0.0.1:8000/account/twitter/login/callback/

    as the Callback URL. Copy the Client-ID and the Client key.

Google
    Login into google and go to https://console.developers.google.com. Create a new project. After the project is created go to Credentials on the left side and configure the OAuth Authorization screen (second tab). Then create the credentials (first tab), more precise a OAuth Client-ID. Use

    ::

        http://127.0.0.1:8000/account/google/login/callback/

    as the Authorized redirect URI. Copy the Client-ID and the Client key.


Add app to RDMO
```````````````

To use the registered app in your RDMO application go to Admin / Social applications / Add social application and

1) choose the corresponding provider

2) give a Name of your choice

3) enter the `Client ID` (or `App ID`) and the `Secret key` (or `Client secret`, `Client key`, `App Secret`)

4) Add your site to the chosen sites.
