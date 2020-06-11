import logging

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rdmo.core.utils import get_next, get_referer_path_info

from .forms import ProfileForm, RemoveForm
from .utils import delete_user

log = logging.getLogger(__name__)


@login_required()
def profile_update(request):
    if settings.PROFILE_UPDATE:
        log.debug('Update user %s', request.user.username)

        form = ProfileForm(request.POST or None, instance=request.user)

        if request.method == 'POST':
            if 'cancel' in request.POST:
                log.debug('User %s uldate cancelled', request.user.username)
                return HttpResponseRedirect(get_next(request))

            if form.is_valid():
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
        log.debug('Remove user form for "%s"', request.user.username)

        form = RemoveForm(request.POST or None, request=request)

        if request.method == 'POST':
            if 'cancel' in request.POST:
                log.debug('User %s removal cancelled', str(request.user))
                return HttpResponseRedirect('/account')

            if form.is_valid():
                log.debug('Deleting user %s', request.user.username)

                if delete_user(request.user, request.POST['email'], request.POST['password']):
                    logout(request)
                    return render(request, 'profile/profile_remove_success.html')
                else:
                    return render(request, 'profile/profile_remove_failed.html')

        return render(request, 'profile/profile_remove_form.html', {
            'form': form,
            'next': get_referer_path_info(request, default='/')
        })
    else:
        return render(request, 'profile/profile_remove_closed.html')


@login_required()
def terms_of_use(request):
    return render(request, 'account/terms_of_use.html')
