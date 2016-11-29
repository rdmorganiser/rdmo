from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.core.utils import get_referer_path_info, get_next

from .forms import ProfileForm


@login_required()
def profile_update(request):
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
