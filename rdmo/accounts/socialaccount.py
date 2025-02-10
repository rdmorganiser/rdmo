from django.conf import settings
from django.contrib.auth.models import Group
from django.forms import BooleanField

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.forms import SignupForm as AllauthSocialSignupForm

from rdmo.accounts.forms import ProfileForm
from rdmo.accounts.models import ConsentFieldValue


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


class SocialSignupForm(AllauthSocialSignupForm, ProfileForm):

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
            if self.cleaned_data['consent']:
                ConsentFieldValue.create_consent(user=user, session=request.session)
