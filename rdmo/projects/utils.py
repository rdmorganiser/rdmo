from rdmo.core.utils import get_ns_tag
from rdmo.domain.models import Attribute
from rdmo.options.models import Option
from rdmo.questions.utils import Catalog

from .models import Project, Membership, Snapshot, Value


def get_answers_tree(project, snapshot=None):

    values = {}
    valuesets = {}

    # first we loop over all values of this snapshot
    # the values are gathered in one nested dict {attribute_id: set_index: collection_index: value}
    # additionally all values with an attribute labeled 'id' are collected in a dict {attribute.parent.id: value.text}

    for value in project.values.filter(snapshot=snapshot):
        if value.attribute:
            # put values in a dict labled by the values attibute id, the set_index and the collection_index
            if value.attribute.id not in values:
                values[value.attribute.id] = {}
            if value.set_index not in values[value.attribute.id]:
                values[value.attribute.id][value.set_index] = {}
            if value.collection_index not in values[value.attribute.id][value.set_index]:
                values[value.attribute.id][value.set_index][value.collection_index] = {}

            values[value.attribute.id][value.set_index][value.collection_index] = value

            # put all values with an attribute labeled 'id' in a valuesets dict labeled by the parent attribute entities id
            if value.attribute.key == 'id':
                if value.attribute.parent.id not in valuesets:
                    valuesets[value.attribute.parent.id] = {}

                valuesets[value.attribute.parent.id][value.set_index] = value.text

    # then we loop over sections, subsections and entities to collect questions and answers

    sections = []
    for catalog_section in project.catalog.sections.order_by('order'):
        subsections = []
        for catalog_subsection in catalog_section.subsections.order_by('order'):
            entities = []
            for catalog_entity in catalog_subsection.entities.filter(question__parent=None).order_by('order'):

                if catalog_entity.attribute_entity:

                    if catalog_entity.is_set:

                        attribute_entity = catalog_entity.attribute_entity

                        if attribute_entity.parent_collection or attribute_entity.is_collection:

                            if attribute_entity.parent_collection:
                                collection = attribute_entity.parent_collection
                            else:
                                collection = attribute_entity

                            questions = []
                            for catalog_question in catalog_entity.questions.order_by('order'):

                                # for a questionset collection loop over valuesets
                                if collection.id in valuesets:

                                    sets = []
                                    for set_index in valuesets[collection.id]:
                                        valueset = valuesets[collection.id][set_index]

                                        # try to get the values for this question's attribute_entity and set_index
                                        answers = get_answers(values, catalog_question.attribute_entity.id, set_index)

                                        if answers:
                                            sets.append({
                                                'id': valueset,
                                                'answers': answers
                                            })

                                    if sets:
                                        questions.append({
                                            'sets': sets,
                                            'text': catalog_question.text,
                                            'attribute': catalog_question.attribute_entity.attribute,
                                            'is_collection': catalog_question.attribute_entity.is_collection or catalog_question.widget_type == 'checkbox'
                                        })

                            if questions:
                                entities.append({
                                    'questions': questions,
                                    'attribute': catalog_entity.attribute_entity,
                                    'is_set': True,
                                    'is_collection': True,
                                })

                        else:
                            # # for a questionset loop over questions
                            questions = []
                            for catalog_question in catalog_entity.questions.order_by('order'):

                                # try to get the values for this question's attribute_entity
                                answers = get_answers(values, catalog_question.attribute_entity.id)

                                if answers:
                                    questions.append({
                                        'text': catalog_question.text,
                                        'attribute': catalog_question.attribute_entity.attribute,
                                        'answers': answers,
                                        'is_collection': catalog_question.attribute_entity.is_collection or catalog_question.widget_type == 'checkbox'
                                    })

                            if questions:
                                entities.append({
                                    'questions': questions,
                                    'attribute': catalog_entity.attribute_entity,
                                    'is_set': True,
                                    'is_collection': False
                                })

                    else:
                        # for a question just collect the answer

                        # try to get the values for this question's attribute_entity
                        answers = get_answers(values, catalog_entity.attribute_entity.id)

                        if answers:
                            entities.append({
                                'text': catalog_entity.question.text,
                                'attribute': catalog_entity.attribute_entity.attribute,
                                'answers': answers,
                                'is_set': False,
                                'is_collection': catalog_entity.attribute_entity.is_collection or catalog_entity.question.widget_type == 'checkbox'
                            })

            if entities:
                subsections.append({
                    'title': catalog_subsection.title,
                    'entities': entities
                })

        if subsections:
            sections.append({
                'title': catalog_section.title,
                'subsections': subsections
            })

    return {'sections': sections}


def get_answers(values, attribute_id, set_index=0):
    answers = []

    try:
        for collection_index, value in sorted(values[attribute_id][set_index].items()):
            answers.append(value.value_and_unit)
    except KeyError:
        pass

    return answers


def import_projects(projects_node, user):

    nsmap = projects_node.nsmap

    for project_node in projects_node.iterchildren():
        import_project(project_node, nsmap, user)


def import_project(project_node, nsmap, user):

    try:
        project = Project.objects.get(title=project_node['title'], user=user)
        print('skipping existing project "%s".' % project_node['title'])
        return
    except Project.DoesNotExist:
        project = Project(title=project_node['title'])

    try:
        catalog_uri = project_node['catalog'].get(get_ns_tag('dc:uri', nsmap))
        project.catalog = Catalog.objects.get(uri=catalog_uri)
    except Catalog.DoesNotExist:
        print('Skipping project "%s". Catalog not found.' % project_node['title'])
        return

    project.description = project_node['description']
    project.created = project_node['created'].text
    project.save()

    # add user to project
    membership = Membership(project=project, user=user, role='admib')
    membership.save()

    # loop over snapshots
    if hasattr(project_node, 'snapshots'):
        for snapshot_node in project_node['snapshots'].iterchildren():
            import_snapshot(snapshot_node, nsmap, project)

    # loop over values
    if hasattr(project_node, 'values'):
        for value_node in project_node['values'].iterchildren():
            import_value(value_node, nsmap, project)


def import_snapshot(snapshot_node, nsmap, project):

    try:
        snapshot = project.snapshots.get(title=snapshot_node['title'])
    except Snapshot.DoesNotExist:
        snapshot = Snapshot(project=project, title=snapshot_node['title'])

    snapshot.description = snapshot_node['description']
    snapshot.created = snapshot_node['created'].text
    snapshot.save()


def import_value(value_node, nsmap, project, snapshot=None):

    try:
        attribute_uri = value_node['attribute'].get(get_ns_tag('dc:uri', nsmap))
        attribute = Attribute.objects.get(uri=attribute_uri)
    except Attribute.DoesNotExist:
        print('Skipping value for Attribute "%s". Attribute not found.' % attribute_uri)
        return

    try:
        value = Value.objects.get(
            project=project,
            snapshot=snapshot,
            attribute=attribute,
            set_index=value_node['set_index'],
            collection_index=value_node['collection_index']
        )
    except Value.DoesNotExist:
        value = Value(
            project=project,
            snapshot=snapshot,
            attribute=attribute,
            set_index=value_node['set_index'],
            collection_index=value_node['collection_index']
        )

    value.created = value_node['created'].text
    value.text = value_node['text']

    try:
        option_uri = value_node['option'].get(get_ns_tag('dc:uri', nsmap))
        value.option = Option.objects.get(uri=option_uri)
    except Option.DoesNotExist:
        value.option = None

    value.save()
