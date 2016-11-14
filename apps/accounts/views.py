from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from apps.core.utils import get_referer, get_next

from .models import AdditionalField
from .forms import UserForm, ProfileForm


@login_required()
def profile_update(request):
    next = get_referer(request)
    additional_fields = AdditionalField.objects.all()

    if request.method == 'POST':
        if 'cancel' in request.POST:
            next = get_next(request)
            return HttpResponseRedirect(next)

        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, user=request.user, additional_fields=additional_fields)

        if user_form.is_valid() and profile_form.is_valid():
            request.user.first_name = user_form.cleaned_data['first_name']
            request.user.last_name = user_form.cleaned_data['last_name']
            request.user.email = user_form.cleaned_data['email']
            request.user.save()

            for additional_field in additional_fields:
                try:
                    additional_value = request.user.additional_values.get(field=additional_field)
                except AdditionalField.DoesNotExist:
                    additional_value = AdditionalField(
                        user=request.user,
                        field=additional_field,
                    )

                additional_value.value = profile_form.cleaned_data[additional_field.key]
                additional_value.save()

            next = get_next(request)
            return HttpResponseRedirect(next)
    else:
        user_initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        }

        user_form = UserForm(initial=user_initial)
        profile_form = ProfileForm(user=request.user, additional_fields=additional_fields)

    return render(request, 'accounts/profile_update_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'next': next
    })
