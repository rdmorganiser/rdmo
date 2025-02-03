"""Terms and Conditions Middleware"""
# ref: https://github.com/cyface/django-termsandconditions/blob/main/termsandconditions/middleware.py

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import ConsentFieldValue

# these exclude url settings are optional
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
        if (
            settings.ACCOUNT_TERMS_OF_USE  # Terms enforcement enabled
            and request.user.is_authenticated
            and request.path != reverse("terms_of_use_accept")
            and self.is_path_protected(request.path)
            and not ConsentFieldValue.has_accepted_terms(request.user, request.session)
        ):
            return HttpResponseRedirect(reverse("terms_of_use_accept"))

        # Proceed with the response for non-protected paths or accepted terms
        return self.get_response(request)

    @staticmethod
    def is_path_protected(path):
        return not (
                any(path.startswith(prefix) for prefix in TERMS_EXCLUDE_URL_PREFIX_LIST) or
                any(substring in path for substring in TERMS_EXCLUDE_URL_CONTAINS_LIST) or
                path in TERMS_EXCLUDE_URL_LIST
        )
