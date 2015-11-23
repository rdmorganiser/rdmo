from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import DetailKey
from .forms import UpdateProfile


@login_required()
def profile(request):
    next = request.META.get('HTTP_REFERER', None)
    detail_keys = DetailKey.objects.all()

    if request.method == 'POST':
        form = UpdateProfile(request.POST, user=request.user, detail_keys=detail_keys, next=next)

        if form.is_valid():
            form_data = form.cleaned_data

            request.user.username = form_data['username']
            request.user.email = form_data['email']
            request.user.first_name = form_data['first_name']
            request.user.last_name = form_data['last_name']
            request.user.save()

            for detail_key in detail_keys:
                if not request.user.profile.details:
                    request.user.profile.details = {}
                request.user.profile.details[detail_key.key] = form_data[detail_key.key]
            request.user.profile.save()

            if form_data['next'] in ['', request.build_absolute_uri()]:
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(form_data['next'])
    else:
        form = UpdateProfile(user=request.user, detail_keys=detail_keys, next=next)

    return render(request, 'accounts/profile_form.html', {'form': form})
