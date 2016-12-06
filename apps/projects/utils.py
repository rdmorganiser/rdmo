import iso8601

from django.utils.translation import ugettext_lazy as _


def get_answers_tree(project, snapshot=None):

    values = {}
    valuesets = {}

    # loop over all values of this snapshot
    for value in project.values.filter(snapshot=snapshot):
        if value.attribute:
            # put values in a dict labled by the values attibute id
            if value.attribute.id not in values:
                values[value.attribute.id] = []
            values[value.attribute.id].append(value)

            # put all values  with an attribute labeled 'id' in a valuesets dict labeled by the parant attribute entities id
            if value.attribute.title == 'id':
                if value.attribute.parent.id not in valuesets:
                    valuesets[value.attribute.parent.id] = {}

                valuesets[value.attribute.parent.id][value.set_index] = value.text

    # loop over sections, subsections and entities to collecti questions and answers
    sections = []
    for catalog_section in project.catalog.sections.order_by('order'):
        subsections = []
        for catalog_subsection in catalog_section.subsections.order_by('order'):
            entities = []
            for catalog_entity in catalog_subsection.entities.filter(question__parent=None).order_by('order'):

                if catalog_entity.attribute_entity:

                    if catalog_entity.is_set:

                        if catalog_entity.attribute_entity.parent_collection:

                            questions = []
                            for catalog_question in catalog_entity.questions.order_by('order'):

                                # for a questionset collection loop over valuesets
                                if catalog_entity.attribute_entity.parent_collection.id in valuesets:

                                    sets = []
                                    for set_index in valuesets[catalog_entity.attribute_entity.parent_collection.id]:
                                        valueset = valuesets[catalog_entity.attribute_entity.parent_collection.id][set_index]

                                        if catalog_question.attribute_entity.id in values:

                                            answers = []
                                            for value in values[catalog_question.attribute_entity.id]:

                                                if value.set_index == set_index:
                                                    answers.append(get_answer(value, catalog_question.attribute_entity.attribute))

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
                            # for a questionset loop over questions
                            questions = []
                            for catalog_question in catalog_entity.questions.order_by('order'):

                                if catalog_question.attribute_entity.id in values:

                                    answers = []
                                    for value in values[catalog_question.attribute_entity.id]:
                                        answers.append(get_answer(value, catalog_question.attribute_entity.attribute))

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
                        # for a questions just collect the answer

                        if catalog_entity.attribute_entity.id in values:

                            answers = []
                            for value in values[catalog_entity.attribute_entity.id]:
                                answers.append(get_answer(value, catalog_entity.attribute_entity.attribute))

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


def get_answer(value, attribute):

    if value.option:
        return value.option.text

    elif value.text:
        if attribute.value_type == 'datetime':
            return iso8601.parse_date(value.text).date()

        elif attribute.value_type == 'boolian':
            if bool(value.text):
                return _('yes')
            else:
                return _('no')

        else:
            return value.text
