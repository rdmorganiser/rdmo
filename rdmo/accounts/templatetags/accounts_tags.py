from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ..utils import get_full_name

register = template.Library()


@register.simple_tag()
def full_name(user):
    return get_full_name(user)


@register.simple_tag()
def user_data_as_dl(user):
    html = '<dl>'
    html += '<dt>{key}</dt><dd>{value}</dd>'.format(
        key=_('Name'),
        value=get_full_name(user),
    )
    for additional_value in user.additional_values.all():
        html += f'<dt>{additional_value.field.text}</dt><dd>{additional_value.value}</dd>'
    html += '</dl>'
    return mark_safe(html)


@register.simple_tag(takes_context=True)
def get_inactive_providers(context={}):
    from allauth.socialaccount.templatetags.socialaccount import get_providers
    if 'form' in context:
        accounts = context['form'].accounts
        providers = [account.provider for account in accounts]
        return [
            provider
            for provider in get_providers(context)
            if provider.id not in providers
        ]
