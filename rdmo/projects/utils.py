import logging

log = logging.getLogger(__name__)


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

            # put all values with an attribute labeled 'id' in a valuesets dict labeled by the parent attribute id
            if value.attribute.key == 'id':
                if value.attribute.parent.id not in valuesets:
                    valuesets[value.attribute.parent.id] = {}

                valuesets[value.attribute.parent.id][value.set_index] = value.text

    # then we loop over sections and questionsets to collect questions and answers
    sections = []
    try:
        project.catalog.sections
    except AttributeError:
        pass
    else:
        for catalog_section in project.catalog.sections.order_by('order'):
            questionsets = []

            for catalog_questionset in catalog_section.questionsets.order_by('order'):

                if catalog_questionset.attribute and catalog_questionset.is_collection:
                    questions = []

                    for catalog_question in catalog_questionset.questions.order_by('order'):
                        sets = []

                        # for a questionset collection loop over valuesets
                        if catalog_questionset.attribute.id in valuesets:

                            for set_index in valuesets[catalog_questionset.attribute.id]:
                                valueset = valuesets[catalog_questionset.attribute.id][set_index]

                                # try to get the values for this question's attribute and set_index
                                answers = get_answers(values, catalog_question.attribute.id, set_index)

                                if answers:
                                    sets.append({
                                        'id': valueset,
                                        'answers': answers
                                    })

                        else:
                            set_index = 0
                            while True:
                                # try to get the values for this question's attribute and set_index
                                answers = get_answers(values, catalog_question.attribute.id, set_index)

                                if answers:
                                    sets.append({
                                        'id': '#%i' % set_index,
                                        'answers': answers
                                    })
                                    set_index += 1
                                else:
                                    break

                        if sets:
                            questions.append({
                                'sets': sets,
                                'text': catalog_question.text,
                                'attribute': catalog_question.attribute,
                                'is_collection': catalog_question.is_collection or catalog_question.widget_type == 'checkbox'
                            })

                    if questions:
                        questionsets.append({
                            'questions': questions,
                            'attribute': catalog_questionset.attribute,
                            'is_collection': True,
                        })

                else:
                    # # for a questionset loop over questions
                    questions = []
                    for catalog_question in catalog_questionset.questions.order_by('order'):

                        # try to get the values for this question's attribute
                        answers = get_answers(values, catalog_question.attribute.id)

                        if answers:
                            questions.append({
                                'text': catalog_question.text,
                                'attribute': catalog_question.attribute,
                                'answers': answers,
                                'is_collection': catalog_question.is_collection or catalog_question.widget_type == 'checkbox'
                            })

                    if questions:
                        questionsets.append({
                            'title': catalog_questionset.title,
                            'questions': questions,
                            'attribute': catalog_questionset.attribute,
                            'is_collection': False
                        })

            if questionsets:
                sections.append({
                    'title': catalog_section.title,
                    'questionsets': questionsets
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


def is_last_owner(project, user):
    # check if user is owner
    if user in project.owners:
        # check if the user is the last owner
        return project.owners.count() <= 1
    else:
        return False


def save_import_values(project, values, checked):
    for value in values:
        if value['value'].attribute:
            value_key = '{value.attribute.uri}[{value.set_index}][{value.collection_index}]'.format(
                value=value['value']
            )

            if value_key in checked:
                current_value = value.get('current')
                if current_value is None:
                    value['value'].project = project
                    value['value'].save()
                else:
                    # make sure we have the correct value
                    assert current_value.snapshot is None
                    assert current_value.attribute == value['value'].attribute
                    assert current_value.set_index == value['value'].set_index
                    assert current_value.collection_index == value['value'].collection_index

                    current_value.text = value['value'].text
                    current_value.option = value['value'].option
                    current_value.value_type = value['value'].value_type
                    current_value.unit = value['value'].unit
                    current_value.save()


def save_import_snapshot_values(project, snapshots, checked):
    for snapshot in snapshots:
        snapshot['snapshot'].project = project
        snapshot['snapshot'].save(copy_values=False)

        for value in snapshot['values']:
            if value['value'].attribute:
                value_key = '{value.attribute.uri}[{snapshot_index}][{value.set_index}][{value.collection_index}]'.format(
                    value=value['value'],
                    snapshot_index=snapshot['index']
                )

                if value_key in checked:
                    value['value'].project = project
                    value['value'].snapshot = snapshot['snapshot']
                    value['value'].save()


def save_import_tasks(project, tasks):
    for task in tasks:
        project.tasks.add(task)


def save_import_views(project, views):
    for view in views:
        project.views.add(view)
