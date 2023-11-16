from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from ..models import Membership

register = template.Library()


@register.simple_tag()
def projects_indent(level):
    string = ''
    if level > 0:
        for i in range(level - 1):
            string += '&ensp;&ensp;'
        string += '&#8226;&ensp;'

    return mark_safe('<span class="projects-indent">' + string + '</span>')


@register.simple_tag()
def project_progress(project):
    if project.progress_count is None or project.progress_total is None:
        return ''

    return _('%(count)s of %(total)s') % {
        'count': project.progress_count,
        'total': project.progress_total
    }

@register.simple_tag()
def project_progress_ratio(project):
    if project.progress_count is None or project.progress_total is None:
        return ''

    try:
        ratio = project.progress_count / project.progress_total
    except ZeroDivisionError:
        ratio = 0

    return f'{ratio:.0%}'


@register.simple_tag()
def project_progress_text(project):
    progress = project_progress(project)
    if progress:
        return _('(%(progress)s progress)') % {'progress': progress}
    else:
        return ''


@register.filter()
@stringfilter
def projects_role(role):
    return dict(Membership.ROLE_CHOICES).get(role, '')
