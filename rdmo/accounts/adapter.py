from django.conf import settings
from django.contrib.auth.models import Group

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


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
