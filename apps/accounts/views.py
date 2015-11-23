try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import DetailKey
from .forms import UserForm, ProfileForm


@login_required()
def profile_update(request):
    next = request.META.get('HTTP_REFERER', None)
    detail_keys = DetailKey.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, profile=request.user.profile, detail_keys=detail_keys)

        if user_form.is_valid() and profile_form.is_valid():
            request.user.first_name = user_form.cleaned_data['first_name']
            request.user.last_name = user_form.cleaned_data['last_name']
            request.user.email = user_form.cleaned_data['email']
            request.user.save()

            for detail_key in detail_keys:
                if not request.user.profile.details:
                    request.user.profile.details = {}
                request.user.profile.details[detail_key.key] = profile_form.cleaned_data[detail_key.key]
            request.user.profile.save()

            next = request.POST.get('next', '')
            path = urlparse(next).path
            if path in ['', reverse('login'), reverse('profile_update')]:
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(next)
    else:
        user_initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }

        user_form = UserForm(initial=user_initial)
        profile_form = ProfileForm(profile=request.user.profile, detail_keys=detail_keys)

    return render(request, 'accounts/profile_update_form.html', {'user_form': user_form, 'profile_form': profile_form, 'next': next})
