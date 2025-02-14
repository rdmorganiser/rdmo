from django.utils.translation import gettext_lazy as _

WIDGET_TYPE_TEXT = 'text'
WIDGET_TYPE_TEXTAREA = 'textarea'
WIDGET_TYPE_YESNO = 'yesno'
WIDGET_TYPE_CHECKBOX = 'checkbox'
WIDGET_TYPE_RADIO = 'radio'
WIDGET_TYPE_SELECT = 'select'
WIDGET_TYPE_SELECT_CREATABLE = 'select_creatable'
WIDGET_TYPE_RANGE = 'range'
WIDGET_TYPE_DATE = 'date'
WIDGET_TYPE_FILE = 'file'
WIDGET_TYPE_CHOICES = (
    (WIDGET_TYPE_TEXT, _('Text')),
    (WIDGET_TYPE_TEXTAREA, _('Textarea')),
    (WIDGET_TYPE_YESNO, _('Yes/No')),
    (WIDGET_TYPE_CHECKBOX, _('Checkboxes')),
    (WIDGET_TYPE_RADIO, _('Radio buttons')),
    (WIDGET_TYPE_SELECT, _('Select drop-down')),
    (WIDGET_TYPE_SELECT_CREATABLE, _('Select drop-down (free)')),
    (WIDGET_TYPE_RANGE, _('Range slider')),
    (WIDGET_TYPE_DATE, _('Date picker')),
    (WIDGET_TYPE_FILE, _('File upload'))
)
