from django import template

register = template.Library()


@register.simple_tag()
def get_question_for_attribute(attribute, questions):
    return questions.filter(attribute=attribute).first()
