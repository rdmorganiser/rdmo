"""Terms and Conditions Middleware"""

# ref: https://github.com/cyface/django-termsandconditions/blob/main/termsandconditions/middleware.py
import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from .utils import user_has_accepted_terms

LOGGER = logging.getLogger(__name__)


ACCEPT_TERMS_PATH = getattr(settings, "ACCEPT_TERMS_PATH", reverse("terms_of_use_update"))
TERMS_EXCLUDE_URL_PREFIX_LIST = getattr(
    settings,
    "TERMS_EXCLUDE_URL_PREFIX_LIST",
    {"/admin", "/i18n", "/static", "/account"},
)
TERMS_EXCLUDE_URL_CONTAINS_LIST = getattr(
    settings, "TERMS_EXCLUDE_URL_CONTAINS_LIST", {}
)
TERMS_EXCLUDE_URL_LIST = getattr(
    settings,
    "TERMS_EXCLUDE_URL_LIST",
    {"/", settings.LOGOUT_URL},
)


class TermsAndConditionsRedirectMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """Process each request to app to ensure terms have been accepted"""

        if not settings.ACCOUNT_TERMS_OF_USE:
            return None  # If terms are not enabled, consider them accepted.

        current_path = request.META["PATH_INFO"]

        if request.user.is_authenticated and is_path_protected(current_path):
            if not user_has_accepted_terms(request.user, request.session):
                # Redirect to update consent page if consent is missing
                return HttpResponseRedirect(reverse("terms_of_use_update"))

        return None


def is_path_protected(path):
    """
    returns True if given path is to be protected, otherwise False

    The path is not to be protected when it appears on:
    TERMS_EXCLUDE_URL_PREFIX_LIST, TERMS_EXCLUDE_URL_LIST, TERMS_EXCLUDE_URL_CONTAINS_LIST or as
    ACCEPT_TERMS_PATH
    """
    protected = True

    for exclude_path in TERMS_EXCLUDE_URL_PREFIX_LIST:
        if path.startswith(exclude_path):
            protected = False

    for contains_path in TERMS_EXCLUDE_URL_CONTAINS_LIST:
        if contains_path in path:
            protected = False

    if path in TERMS_EXCLUDE_URL_LIST:
        protected = False

    if path.startswith(ACCEPT_TERMS_PATH):
        protected = False

    return protected
