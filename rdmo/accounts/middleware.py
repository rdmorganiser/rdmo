"""Terms and Conditions Middleware"""
# ref: https://github.com/cyface/django-termsandconditions/blob/main/termsandconditions/middleware.py

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import ConsentFieldValue


class TermsAndConditionsRedirectMiddleware:
    """Middleware to ensure terms and conditions have been accepted."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            settings.ACCOUNT_TERMS_OF_USE  # Terms enforcement enabled
            and request.user.is_authenticated
            and self.is_path_protected(request.path)
            and not ConsentFieldValue.has_accepted_terms(request.user, request.session)
        ):
            return HttpResponseRedirect(reverse("terms_of_use_accept"))

        # Proceed with the response for non-protected paths or accepted terms
        return self.get_response(request)

    @staticmethod
    def is_path_protected(path):
        # all paths should be protected, except what is excluded here
        return not (
                path == reverse("terms_of_use_accept") or
                any(path.startswith(prefix) for prefix in settings.ACCOUNT_TERMS_OF_USE_EXCLUDE_URL_PREFIXES) or
                any(substring in path for substring in settings.ACCOUNT_TERMS_OF_USE_EXCLUDE_URL_CONTAINS) or
                path in settings.ACCOUNT_TERMS_OF_USE_EXCLUDE_URLS
        )
