from rdmo.questions.widgets import Widget


class TextWidget(Widget):
    template_name = 'projects/project_questions_form_group_text.html'
    widget_class = 'text'


class TextareaWidget(Widget):
    template_name = 'projects/project_questions_form_group_textarea.html'
    widget_class = 'text'


class YesnoWidget(Widget):
    template_name = 'projects/project_questions_form_group_yesno.html'
    widget_class = 'yesno'


class RadioWidget(Widget):
    template_name = 'projects/project_questions_form_group_radio.html'
    widget_class = 'radio'


class SelectWidget(Widget):
    template_name = 'projects/project_questions_form_group_select.html'
    widget_class = 'select'


class AutocompleteWidget(Widget):
    template_name = 'projects/project_questions_form_group_autocomplete.html'
    widget_class = 'autocomplete'


class DateWidget(Widget):
    template_name = 'projects/project_questions_form_group_date.html'
    widget_class = 'date'


class RangeWidget(Widget):
    template_name = 'projects/project_questions_form_group_range.html'
    widget_class = 'range'


class CheckboxWidget(Widget):
    template_name = 'projects/project_questions_form_group_checkbox.html'
    widget_class = 'checkbox'


class FileWidget(Widget):
    template_name = 'projects/project_questions_form_group_file.html'
    widget_class = 'file'
