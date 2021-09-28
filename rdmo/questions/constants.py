from django.utils.translation import gettext_lazy as _

WIDGET_TYPES = (
    ('text', _('Text')),
    ('textarea', _('Textarea')),
    ('yesno', _('Yes/No')),
    ('checkbox', _('Checkboxes')),
    ('radio', _('Radio buttons')),
    ('select', _('Select drop-down')),
    ('autocomplete', _('Autocomplete')),
    ('range', _('Range slider')),
    ('date', _('Date picker')),
    ('file', _('File upload'))
)
