"""Terms and Conditions Middleware"""
# ref: https://github.com/cyface/django-termsandconditions/blob/main/termsandconditions/middleware.py
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .utils import user_has_accepted_terms

LOGGER = logging.getLogger(__name__)

ACCEPT_TERMS_PATH = getattr(settings, "ACCEPT_TERMS_PATH", reverse("terms_of_use_update"))
TERMS_EXCLUDE_URL_PREFIX_LIST = getattr(
    settings,
    "TERMS_EXCLUDE_URL_PREFIX_LIST",
    ["/admin", "/i18n", "/static", "/account"],
)
TERMS_EXCLUDE_URL_CONTAINS_LIST = getattr(settings, "TERMS_EXCLUDE_URL_CONTAINS_LIST", [])
TERMS_EXCLUDE_URL_LIST = getattr(
    settings,
    "TERMS_EXCLUDE_URL_LIST",
    ["/", settings.LOGOUT_URL],
)


class TermsAndConditionsRedirectMiddleware:
    """Middleware to ensure terms and conditions have been accepted."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip processing if ACCOUNT_TERMS_OF_USE is disabled
        if not getattr(settings, "ACCOUNT_TERMS_OF_USE", False):
            return self.get_response(request)

        # check if the current path is protected
        if (
            request.user.is_authenticated
            and self.is_path_protected(request.path)
            and not user_has_accepted_terms(request.user, request.session)
        ):
            return HttpResponseRedirect(ACCEPT_TERMS_PATH)

        # Proceed with the response for non-protected paths or accepted terms
        return self.get_response(request)

    @staticmethod
    def is_path_protected(path):
        """
        Determine if a given path is protected by the middleware.

        Paths are excluded if they match any of the following:
        - Start with a prefix in TERMS_EXCLUDE_URL_PREFIX_LIST
        - Contain a substring in TERMS_EXCLUDE_URL_CONTAINS_LIST
        - Are explicitly listed in TERMS_EXCLUDE_URL_LIST
        - Start with the ACCEPT_TERMS_PATH
        """
        if any(path.startswith(prefix) for prefix in TERMS_EXCLUDE_URL_PREFIX_LIST):
            return False

        if any(substring in path for substring in TERMS_EXCLUDE_URL_CONTAINS_LIST):
            return False

        if path in TERMS_EXCLUDE_URL_LIST:
            return False

        if path.startswith(ACCEPT_TERMS_PATH):
            return False

        return True
