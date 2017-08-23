from rdmo.core.utils import get_ns_tag
from rdmo.domain.models import AttributeEntity

from .models import Catalog, Section, Subsection, QuestionEntity, Question


def import_catalog(catalog_node):

    nsmap = catalog_node.nsmap

    catalog_uri = catalog_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        catalog = Catalog.objects.get(uri=catalog_uri)
    except Catalog.DoesNotExist:
        catalog = Catalog()

    catalog.uri_prefix = catalog_uri.split('/questions/')[0]
    catalog.key = catalog_uri.split('/')[-1]
    catalog.comment = catalog_node[get_ns_tag('dc:comment', nsmap)]
    catalog.order = catalog_node['order']
    for element in catalog_node.title:
        setattr(catalog, 'title_' + element.get('lang'), element.text)

    catalog.save()

    if hasattr(catalog_node, 'sections'):
        for section_node in catalog_node.sections.iterchildren():
            import_section(section_node, nsmap, catalog=catalog)


def import_section(section_node, nsmap, catalog=None):
    section_uri = section_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        section = Section.objects.get(uri=section_uri)
    except Section.DoesNotExist:
        section = Section()

    section.uri_prefix = section_uri.split('/questions/')[0]
    section.key = section_uri.split('/')[-1]
    section.comment = section_node[get_ns_tag('dc:comment', nsmap)]
    section.catalog = catalog
    section.order = section_node['order']
    for element in section_node.title:
        setattr(section, 'title_' + element.get('lang'), element.text)

    section.save()

    if hasattr(section_node, 'subsections'):
        for subsection_node in section_node.subsections.iterchildren():
            import_subsection(subsection_node, nsmap, section=section)


def import_subsection(subsection_node, nsmap, section=None):
    subsection_uri = subsection_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        subsection = Subsection.objects.get(uri=subsection_uri)
    except Subsection.DoesNotExist:
        subsection = Subsection()

    subsection.uri_prefix = subsection_uri.split('/questions/')[0]
    subsection.key = subsection_uri.split('/')[-1]
    subsection.comment = subsection_node[get_ns_tag('dc:comment', nsmap)]
    subsection.section = section
    subsection.order = subsection_node['order']
    for element in subsection_node.title:
        setattr(subsection, 'title_' + element.get('lang'), element.text)

    subsection.save()

    if hasattr(subsection_node, 'entities'):
        for entity_node in subsection_node.entities.iterchildren():
            if entity_node.tag == 'questionset':
                import_questionset(entity_node, nsmap, subsection=subsection)
            else:
                import_question(entity_node, nsmap, subsection=subsection)


def import_questionset(questionset_node, nsmap, subsection=None):
    questionset_uri = questionset_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        questionset = QuestionEntity.objects.get(uri=questionset_uri)
    except QuestionEntity.DoesNotExist:
        questionset = QuestionEntity()

    questionset.uri_prefix = questionset_uri.split('/questions/')[0]
    questionset.key = questionset_uri.split('/')[-1]
    questionset.comment = questionset_node[get_ns_tag('dc:comment', nsmap)]
    questionset.subsection = subsection
    questionset.order = questionset_node['order']
    for element in questionset_node['help']:
        setattr(questionset, 'help_' + element.get('lang'), element.text)
    try:
        attribute_entity_uri = questionset_node['attribute_entity'].get(get_ns_tag('dc:uri', nsmap))
        questionset.attribute_entity = AttributeEntity.objects.get(uri=attribute_entity_uri)
    except (AttributeError, AttributeEntity.DoesNotExist):
        questionset.attribute_entity = None

    questionset.save()

    if hasattr(questionset_node, 'questions'):
        for question_node in questionset_node.questions.iterchildren():
            import_question(question_node, nsmap, subsection=subsection, parent=questionset)


def import_question(question_node, nsmap, subsection=None, parent=None):
    question_uri = question_node[get_ns_tag('dc:uri', nsmap)].text

    try:
        question = Question.objects.get(uri=question_uri)
    except Question.DoesNotExist:
        question = Question()

    question.uri_prefix = question_uri.split('/questions/')[0]
    question.key = question_uri.split('/')[-1]
    question.comment = question_node[get_ns_tag('dc:comment', nsmap)]
    question.subsection = subsection
    question.parent = parent
    question.order = question_node['order']
    question.widget_type = question_node.widget_type
    for element in question_node['text']:
        setattr(question, 'text_' + element.get('lang'), element.text)
    for element in question_node['help']:
        setattr(question, 'help_' + element.get('lang'), element.text)
    try:
        attribute_entity_uri = question_node['attribute_entity'].get(get_ns_tag('dc:uri', nsmap))
        question.attribute_entity = AttributeEntity.objects.get(uri=attribute_entity_uri)
    except (AttributeError, AttributeEntity.DoesNotExist):
        question.attribute_entity = None

    question.save()
