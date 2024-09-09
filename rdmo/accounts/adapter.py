from django.conf import settings
from django.contrib.auth.models import Group
from django.forms import BooleanField

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .forms import ProfileForm
from .models import ConsentFieldValue


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return settings.ACCOUNT_SIGNUP

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)

        if settings.ACCOUNT_GROUPS:
            groups = Group.objects.filter(name__in=settings.ACCOUNT_GROUPS)
            user.groups.set(groups)

        return user

class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return settings.SOCIALACCOUNT_SIGNUP

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        if settings.SOCIALACCOUNT_GROUPS:
            provider = str(sociallogin.account.provider)
            groups = Group.objects.filter(name__in=settings.SOCIALACCOUNT_GROUPS.get(provider, []))
            user.groups.set(groups)

        return user


class LoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove forget password link introduced with allauth 0.57.0
        password_field = self.fields.get('password')
        if password_field:
            password_field.help_text = None


class SignupForm(AllauthSignupForm, ProfileForm):

    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add a consent field, the label is added in the template
        if settings.ACCOUNT_TERMS_OF_USE:
            self.fields['consent'] = BooleanField(required=True)

    def signup(self, request, user):
        self._save_additional_values(user)

        # store the consent field
        if settings.ACCOUNT_TERMS_OF_USE:
            consent = ConsentFieldValue(user=user, consent=self.cleaned_data['consent'])
            consent.save()
