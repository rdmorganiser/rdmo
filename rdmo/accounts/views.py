import logging
import re

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from rest_framework.authtoken.models import Token

from rdmo.core.utils import get_next, get_referer_path_info

from .forms import AcceptConsentForm, ProfileForm, RemoveForm
from .models import ConsentFieldValue
from .utils import delete_user

log = logging.getLogger(__name__)


@login_required()
def profile_update(request):
    if settings.PROFILE_UPDATE:
        log.debug('Update user %s', request.user.username)

        form = ProfileForm(request.POST or None, instance=request.user)

        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponseRedirect(get_next(request))

        return render(request, 'profile/profile_update_form.html', {
            'form': form,
            'next': get_referer_path_info(request, default='/')
        })
    else:
        return render(request, 'profile/profile_update_closed.html')


@login_required()
def remove_user(request):
    if settings.PROFILE_DELETE:
        log.debug('Remove user %s', request.user.username)

        form = RemoveForm(request.POST or None, user=request.user)
        print(request.POST)

        if request.method == 'POST' and form.is_valid():
            user_is_deleted = delete_user(user=request.user,
                                          email=request.POST['email'],
                                          password=request.POST.get('password', None))

            if user_is_deleted:
                logout(request)
                return render(request, 'profile/profile_remove_success.html')
            else:
                log.info('Remove user, deletion failed for %s', request.user.username)
                return render(request, 'profile/profile_remove_failed.html')

        return render(request, 'profile/profile_remove_form.html', {
            'form': form,
            'next': get_referer_path_info(request, default='/')
        })
    else:
        return render(request, 'profile/profile_remove_closed.html')


def terms_of_use(request):
    return render(request, 'account/terms_of_use.html')


@login_required()
def token(request):
    if request.method == 'POST':
        try:
            Token.objects.get(user=request.user).delete()
        except Token.DoesNotExist:
            pass

    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'account/account_token.html', {
        'token': token
    })


def shibboleth_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('projects'))
    else:
        login_url = settings.SHIBBOLETH_LOGIN_URL + f'?target={request.path}'
        return HttpResponseRedirect(login_url)


def shibboleth_logout(request):
    logout_url = reverse('account_logout')
    if settings.SHIBBOLETH_USERNAME_PATTERN is None \
            or re.search(settings.SHIBBOLETH_USERNAME_PATTERN, request.user.username):
        logout_url += f'?next={settings.SHIBBOLETH_LOGOUT_URL}'
    return HttpResponseRedirect(logout_url)


def terms_of_use_accept(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    # Use the form to handle both update and delete actions
    form = AcceptConsentForm(request.POST or None, user=request.user)

    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            print(2)
            consent_saved = form.save(request.session)  # saves the consent and sets the session key
            if consent_saved:
                return redirect("home")

    return render(request, "account/terms_of_use_accept.html", {
        "form": form,
        "has_consented": ConsentFieldValue.objects.filter(user=request.user).exists()
    })
