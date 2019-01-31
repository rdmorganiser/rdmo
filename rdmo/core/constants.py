from django.utils.translation import ugettext_lazy as _

VALUE_TYPE_TEXT = 'text'
VALUE_TYPE_URL = 'url'
VALUE_TYPE_INTEGER = 'integer'
VALUE_TYPE_FLOAT = 'float'
VALUE_TYPE_BOOLEAN = 'boolean'
VALUE_TYPE_DATETIME = 'datetime'
VALUE_TYPE_OPTIONS = 'option'
VALUE_TYPE_CHOICES = (
    (VALUE_TYPE_TEXT, _('Text')),
    (VALUE_TYPE_URL, _('URL')),
    (VALUE_TYPE_INTEGER, _('Integer')),
    (VALUE_TYPE_FLOAT, _('Float')),
    (VALUE_TYPE_BOOLEAN, _('Boolean')),
    (VALUE_TYPE_DATETIME, _('Datetime')),
    (VALUE_TYPE_OPTIONS, _('Option'))
)
