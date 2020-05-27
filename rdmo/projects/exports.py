import re

from django.http import HttpResponse
from rdmo.core.exports import prettify_xml
from rdmo.core.utils import render_to_csv

from .renderers import XMLRenderer
from .serializers.export import ProjectSerializer as ExportSerializer
from .utils import get_answers_tree


class Export(object):

    def __init__(self, project):
        self.project = project

    def render(self):
        raise NotImplementedError


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


class XMLExport(Export):

    def render(self):
        serializer = ExportSerializer(self.project)
        xmldata = XMLRenderer().render(serializer.data)
        response = HttpResponse(prettify_xml(xmldata), content_type="application/xml")
        response['Content-Disposition'] = 'filename="%s.xml"' % self.project.title
        return response


class MaDMPExport(Export):

    def render(self):
        return HttpResponse('madmp')
