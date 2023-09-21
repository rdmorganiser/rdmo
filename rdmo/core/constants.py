from django.utils.translation import gettext_lazy as _

VALUE_TYPE_TEXT = 'text'
VALUE_TYPE_URL = 'url'
VALUE_TYPE_INTEGER = 'integer'
VALUE_TYPE_FLOAT = 'float'
VALUE_TYPE_BOOLEAN = 'boolean'
VALUE_TYPE_DATETIME = 'datetime'
VALUE_TYPE_OPTIONS = 'option'
VALUE_TYPE_EMAIL = 'email'
VALUE_TYPE_PHONE = 'phone'
VALUE_TYPE_FILE = 'file'
VALUE_TYPE_CHOICES = (
    (VALUE_TYPE_TEXT, _('Text')),
    (VALUE_TYPE_URL, _('URL')),
    (VALUE_TYPE_INTEGER, _('Integer')),
    (VALUE_TYPE_FLOAT, _('Float')),
    (VALUE_TYPE_BOOLEAN, _('Boolean')),
    (VALUE_TYPE_DATETIME, _('Datetime')),
    (VALUE_TYPE_EMAIL, _('E-mail')),
    (VALUE_TYPE_PHONE, _('Phone')),
    (VALUE_TYPE_OPTIONS, _('Option')),
    (VALUE_TYPE_FILE, _('File'))
)

PERMISSIONS = {
    'conditions.condition': (
        'conditions.add_condition', 'conditions.change_condition', 'conditions.delete_condition'
    ),
    'domain.attribute': (
        'domain.add_attribute', 'domain.change_attribute', 'domain.delete_attribute'
    ),
    'options.optionset': (
        'options.add_optionset', 'options.change_optionset', 'options.delete_optionset'
    ),
    'options.option': (
        'options.add_option', 'options.change_option', 'options.delete_option'
    ),
    'questions.catalog': (
        'questions.add_catalog', 'questions.change_catalog', 'questions.delete_catalog'
    ),
    'questions.section': (
        'questions.add_section', 'questions.change_section', 'questions.delete_section'
    ),
    'questions.page': (
        'questions.add_page', 'questions.change_page', 'questions.delete_page'
    ),
    'questions.questionset': (
        'questions.add_questionset', 'questions.change_questionset', 'questions.delete_questionset'
    ),
    'questions.question': (
        'questions.add_question', 'questions.change_question', 'questions.delete_question'
    ),
    'tasks.task': (
        'tasks.add_task', 'tasks.change_task', 'tasks.delete_task'
    ),
    'views.view': (
        'views.add_view', 'views.change_view', 'views.delete_view'
    )
}
