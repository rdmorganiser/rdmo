from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QuestionsConfig(AppConfig):
    name = 'rdmo.questions'
    verbose_name = _('Questions')
