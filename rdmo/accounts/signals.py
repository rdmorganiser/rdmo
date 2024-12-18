from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.urls import reverse

from .utils import user_has_accepted_terms


@receiver(user_logged_in)
def check_user_consent(sender, request, user, **kwargs):
    # check consent and store it in the session
    if not user_has_accepted_terms(user, request.session):
        return HttpResponseRedirect(reverse("terms_of_use_update"))
