import re

from django.utils.translation import gettext_lazy as _

from rdmo.core.utils import render_to_csv, render_to_json
from rdmo.views.templatetags import view_tags
from rdmo.views.utils import ProjectWrapper

from . import Export


class AnswersExportMixin:
    download = True

    def get_data(self):
        # prefetch most elements of the catalog
        self.project.catalog.prefetch_elements()

        # create project wrapper as for the views
        project_wrapper = ProjectWrapper(self.project, self.snapshot)

        data = []
        for question in project_wrapper.questions:
            # use the same template tags as in project_answers_element.html
            # get labels and to correctly attribute for conditions
            set_prefixes = view_tags.get_set_prefixes({}, question['attribute'], project=project_wrapper)
            for set_prefix in set_prefixes:
                set_indexes = view_tags.get_set_indexes({}, question['attribute'], set_prefix=set_prefix,
                                                        project=project_wrapper)
                for set_index in set_indexes:
                    values = view_tags.get_values(
                        {}, question['attribute'], set_prefix=set_prefix, set_index=set_index, project=project_wrapper
                    )
                    labels = view_tags.get_labels(
                        {}, question, set_prefix=set_prefix, set_index=set_index, project=project_wrapper
                    )
                    result = view_tags.check_element(
                        {}, question, set_prefix=set_prefix, set_index=set_index, project=project_wrapper
                    )
                    if result:
                        data.append({
                            'question': self.stringify(question['text']),
                            'set': ' '.join(labels),
                            'values': self.stringify_values(values)
                        })

        return data

    def stringify_values(self, values):
        if values is not None:
            return '; '.join([self.stringify(value['value_and_unit']) for value in values])
        else:
            return ''

    def stringify(self, el):
        if el is None:
            return ''
        else:
            return re.sub(r'\s+', ' ', str(el))


class CSVExport(AnswersExportMixin, Export):
    delimiter = ','

    def render(self):
        rows = [item.values() for item in self.get_data()]
        return render_to_csv(self.project.title, rows, self.delimiter)


class CSVCommaExport(CSVExport):
    label = _('CSV (comma separated)')
    description = _('Export the answers of the project as a CSV file with comma separated values.')

    delimiter = ','


class CSVSemicolonExport(CSVExport):
    label = _('CSV (semicolon separated)')
    description = _('Export the answers of the project as a CSV file with semicolon separated values.')

    delimiter = ';'


class JSONExport(AnswersExportMixin, Export):
    label = _('JSON')
    description = _('Export the answers of the project as a JSON file.')

    def render(self):
        return render_to_json(self.project.title, self.get_data())
