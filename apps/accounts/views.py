from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.core.utils import get_referer_url_name, get_next_redirect

from .forms import ProfileForm


@login_required()
def profile_update(request):
    next = get_referer_url_name(request, 'home')

    form = ProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return get_next_redirect(request)

        if form.is_valid():
            form.save()
            return get_next_redirect(request)

    return render(request, 'profile/profile_update_form.html', {
        'form': form,
        'next': next
    })
