import re

from django.http import HttpResponse
from rdmo.core.exports import prettify_xml
from rdmo.core.utils import render_to_csv

from .renderers import XMLRenderer
from .serializers.export import ProjectSerializer as ExportSerializer
from .utils import get_answers_tree


class Export(object):

    def __init__(self, project, snapshot=None):
        self.project = project
        self.snapshot = snapshot
        self.values = self.project.values.filter(snapshot=self.snapshot)

    def render(self):
        raise NotImplementedError

    def get_set(self, path):
        return self.values.filter(attribute__path=path)

    def get_values(self, path, set_index=0):
        return self.values.filter(attribute__path=path, set_index=set_index)

    def get_value(self, path, set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_index)[collection_index]
        except IndexError:
            return None

    def get_text(self, path, set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_index)[collection_index].text
        except IndexError:
            return None

    def get_timestamp(self, path, set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_index)[collection_index].value.isoformat()
        except (IndexError, AttributeError):
            return None

    def get_year(self, path, set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_index)[collection_index].value.year
        except (IndexError, AttributeError):
            return None

    def get_list(self, path, set_index=0):
        values = self.get_values(path, set_index)
        return [value.text for value in values if value.text]

    def get_bool(self, path, set_index=0, collection_index=0):
        value = self.get_value(path, set_index, collection_index)
        if value:
            return True if value.text == '1' else False
        else:
            return None

    def get_option(self, options, path, set_index=0, collection_index=0, default=None):
        value = self.get_value(path, set_index, collection_index)
        if value and value.option:
            # lookup option dict in class
            return options.get(value.option.path, default)
        else:
            return default


class CSVExport(Export):

    delimiter = ','

    def render(self):
        data = []
        answer_sections = get_answers_tree(self.project).get('sections')
        for section in answer_sections:
            questionsets = section.get('questionsets')
            for questionset in questionsets:
                questions = questionset.get('questions')
                for question in questions:
                    text = self.stringify(question.get('text'))
                    answers = self.stringify_answers(question.get('answers'))
                    data.append((text, answers))

        return render_to_csv(self.project.title, data, self.delimiter)

    def stringify_answers(self, answers):
        if answers is not None:
            return '; '.join([self.stringify(answer) for answer in answers])
        else:
            return ''

    def stringify(self, el):
        if el is None:
            return ''
        else:
            return re.sub(r'\s+', ' ', str(el))


class CSVCommaExport(CSVExport):
    delimiter = ','


class CSVSemicolonExport(CSVExport):
    delimiter = ';'


class RDMOXMLExport(Export):

    def render(self):
        serializer = ExportSerializer(self.project)
        xmldata = XMLRenderer().render(serializer.data)
        response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
        response['Content-Disposition'] = 'filename="%s.xml"' % self.project.title
        return response
