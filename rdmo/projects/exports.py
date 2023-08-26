import re

from django.http import HttpResponse

from rdmo.core.exports import prettify_xml
from rdmo.core.plugins import Plugin
from rdmo.core.utils import render_to_csv, render_to_json
from rdmo.views.templatetags import view_tags
from rdmo.views.utils import ProjectWrapper

from .renderers import XMLRenderer
from .serializers.export import ProjectSerializer as ExportSerializer


class Export(Plugin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = None
        self.snapshot = None

    def render(self):
        raise NotImplementedError

    def submit(self):
        raise NotImplementedError

    def get_set(self, path, set_prefix=''):
        return self.project.values.filter(snapshot=self.snapshot, attribute__path=path, set_prefix=set_prefix) \
                                  .order_by('set_index', 'collection_index')

    def get_values(self, path, set_prefix='', set_index=0):
        return self.project.values.filter(snapshot=self.snapshot, attribute__path=path,
                                          set_prefix=set_prefix, set_index=set_index) \
                                  .order_by('collection_index')

    def get_value(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index]
        except IndexError:
            return None

    def get_text(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index].text
        except IndexError:
            return None

    def get_timestamp(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index].value.isoformat()
        except (IndexError, AttributeError):
            return None

    def get_year(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index].value.year
        except (IndexError, AttributeError):
            return None

    def get_list(self, path, set_prefix='', set_index=0):
        values = self.get_values(path, set_prefix=set_prefix, set_index=set_index)
        return [value.text for value in values if value.text]

    def get_bool(self, path, set_prefix='', set_index=0, collection_index=0):
        value = self.get_value(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        if value:
            return True if value.text == '1' else False
        else:
            return None

    def get_option(self, options, path, set_prefix='', set_index=0, collection_index=0, default=None):
        value = self.get_value(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        if value and value.option:
            # lookup option dict in class
            return options.get(value.option.path, default)
        else:
            return default


class AnswersExportMixin:

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
    delimiter = ','


class CSVSemicolonExport(CSVExport):
    delimiter = ';'


class JSONExport(AnswersExportMixin, Export):

    def render(self):
        return render_to_json(self.project.title, self.get_data())


class RDMOXMLExport(Export):

    def render(self):
        serializer = ExportSerializer(self.project)
        xmldata = XMLRenderer().render(serializer.data)
        response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
        response['Content-Disposition'] = 'filename="%s.xml"' % self.project.title
        return response
