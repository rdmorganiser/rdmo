from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.simple_tag()
def get_answer_for_question(question, answers_dict):
    if question.pk in answers_dict:
        return answers_dict[question.pk].text
    else:
        return _('Not answered yet.')
