import sys
from importlib import import_module, reload

import pytest

from django.core.management import call_command
from django.db import connection
from django.urls import clear_url_caches, get_resolver, reverse


def reload_urlconf(urlconf=None, settings=None):
    clear_url_caches()

    if urlconf is None and settings is None:
        from django.conf import settings
        urlconf = settings.ROOT_URLCONF
    elif urlconf is None and settings is not None:
        # take the settings during pytest run
        urlconf = settings.ROOT_URLCONF

    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
    else:
        import_module(urlconf)


def reload_urls(*app_names: str, settings = None) -> None:
    # reload the urlconf of the app
    for _app in app_names:
        reload_urlconf(urlconf=_app, settings=settings)

    # reload the core urlconf
    reload_urlconf(urlconf='rdmo.core.urls', settings=settings)

    # reload the testcase settings urlconf
    reload_urlconf(settings=settings)

    get_resolver()._populate()


@pytest.fixture(autouse=False)
def enable_terms_of_use(settings):  # noqa: PT004
    settings.ACCOUNT_TERMS_OF_USE = True
    settings.MIDDLEWARE += [
        settings.ACCOUNT_TERMS_OF_USE_MIDDLEWARE
    ]
    reload_urls('rdmo.accounts.urls')

    yield

    # revert settings to initial state
    settings.ACCOUNT_TERMS_OF_USE = False
    settings.MIDDLEWARE.remove(settings.ACCOUNT_TERMS_OF_USE_MIDDLEWARE)
    # 🔹 Reload URLs to reflect the changes
    reload_urls('rdmo.accounts.urls')


@pytest.fixture(autouse=False)
def enable_socialaccount(db, client, settings, django_db_setup, django_db_blocker, django_db_use_migrations):  # noqa: PT004
    # Arrange: this fixture enable and initializes the allauth.sociallaccounts
    # use this fixture with the decorator @pytest.mark.django_db(transaction=True) on your tests

    # Detect if --no-migrations is being used
    if not django_db_use_migrations and connection.vendor == 'sqlite':
        pytest.xfail("This test is expected to fail when --no-migrations is enabled.")

    settings.SOCIALACCOUNT = True
    settings.SOCIALACCOUNT_SIGNUP = True
    # 🔹 Add required apps
    added_apps = [
        "allauth.socialaccount",
        "allauth.socialaccount.providers.dummy",
    ]
    new_apps = [app for app in added_apps if app not in settings.INSTALLED_APPS]

    if new_apps:
        settings.INSTALLED_APPS += new_apps

        # 🔹 Force Django to reload apps
        import django
        from django.apps import apps
        apps.clear_cache()
        django.setup()

    with django_db_blocker.unblock():
        call_command("migrate")

    # 🔹 Reload URL patterns manually
    clear_url_caches()
    reload_urls('allauth.urls', 'rdmo.accounts.urls',settings=settings)
    # 🔹 Verify that the route now exists
    assert reverse("dummy_login")  # Ensure the route exists

    # Check database backend
    db_backend = connection.vendor  # 'sqlite', 'mysql', or 'postgresql'

    if db_backend == "sqlite":
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys=OFF;")  # Disable FKs in SQLite

    from allauth.socialaccount.models import SocialAccount
    assert SocialAccount.objects.exists() is not None  # Ensure table exists before using it

    yield  # Run test

    # 🔹 Cleanup: Remove added apps and reset settings
    settings.INSTALLED_APPS.remove("allauth.socialaccount")
    settings.INSTALLED_APPS.remove("allauth.socialaccount.providers.dummy")

    settings.SOCIALACCOUNT = False
    settings.SOCIALACCOUNT_SIGNUP = False

    # 🔹 Force Django to reload apps again
    import django
    from django.apps import apps
    apps.clear_cache()
    django.setup()

    reload_urls('allauth.urls', 'rdmo.accounts.urls', settings=settings)

    # **Teardown: Apply only for SQLite**
    if db_backend == "sqlite":
        with django_db_blocker.unblock():
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA foreign_keys=OFF;")  # Disable FKs before flush
            try:
                call_command("flush", "--no-input")  # Reset DB
            finally:
                with connection.cursor() as cursor:
                    cursor.execute("PRAGMA foreign_keys=ON;")  # Re-enable FKs
    else:
        # For MySQL & PostgreSQL, just run normal flush
        call_command("flush", "--no-input", allow_cascade=True)
