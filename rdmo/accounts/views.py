import logging

from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rdmo.core.utils import get_referer_path_info, get_next

from .forms import ProfileForm, RemoveForm

log = logging.getLogger(__name__)


@login_required()
def profile_update(request):
    if settings.PROFILE_UPDATE:
        form = ProfileForm(request.POST or None, instance=request.user)

        if request.method == 'POST':
            if 'cancel' in request.POST:
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
    log.info('Remove user %s', str(request.user))
    form = RemoveForm(request.POST or None, request=request)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            log.info('User %s removal cancelled', str(request.user))
            return HttpResponseRedirect('/account')

        if form.is_valid():
            log.info("Valid form. Deleting user.")
            templ = delete_user(request)
            return render(request, templ)

    return render(request, 'profile/profile_remove_form.html', {
        'form': form,
        'next': get_referer_path_info(request, default='/')
    })


@login_required
def delete_user(request):
    password = request.POST['password']
    if not request.user.check_password(password):
        log.info('Invalid password')
        return 'profile/profile_remove_failed.html'
    else:
        try:
            # request.user.delete()
            log.info('The user is deleted')
            return 'profile/profile_remove_success.html'

        except User.DoesNotExist:
            log.info('User does not exist')
            return 'profile/profile_remove_failed.html'

        except Exception as e:
            log.info(e)
            return 'profile/profile_remove_failed.html'
