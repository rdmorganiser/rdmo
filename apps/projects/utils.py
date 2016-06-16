
def get_answer_tree(project):

    values = {}
    sets = {}

    # loop over all values of this snapshot
    for value in project.current_snapshot.values.all():

        # put values in a dict labled by the values attibute id
        if value.attribute.id not in values:
            values[value.attribute.id] = []
        values[value.attribute.id].append(value)

        # put all values  with an attribute labeled 'id' in a sets dict labeled by the parant attribute entities id
        if value.attribute.title == 'id':
            if value.attribute.parent_entity.id not in sets:
                sets[value.attribute.parent_entity.id] = {}

            sets[value.attribute.parent_entity.id][value.set_index] = value.text

    # loop over sections, subsections and entities to collecti questions and answers
    sections = []
    for catalog_section in project.catalog.sections.order_by('order'):
        subsections = []
        for catalog_subsection in catalog_section.subsections.order_by('order'):
            entities = []
            for catalog_entity in catalog_subsection.entities.filter(question__parent_entity=None).order_by('order'):

                # for a questionset loop over questions and for set collections prepend the sets title
                if catalog_entity.is_set:

                    questions = []
                    for catalog_question in catalog_entity.questions.order_by('order'):

                        if catalog_question.attribute_entity.id in values:

                            answers = []
                            for value in values[catalog_question.attribute_entity.id]:

                                answer = ''
                                if catalog_entity.is_collection and sets[catalog_entity.attribute_entity.id]:
                                    answer += '(%s) ' % sets[catalog_entity.attribute_entity.id][value.set_index]

                                if value.option:
                                    answer += value.option.text
                                elif value.text:
                                    answer += value.text

                                answers.append(answer)

                            if answers:
                                questions.append({
                                    'text': catalog_question.text,
                                    'attribute': catalog_question.attribute_entity.full_title,
                                    'answers': answers,
                                })

                    if questions:
                        entities.append({
                            'questions': questions,
                            'attribute': catalog_entity.attribute_entity.full_title,
                            'is_set': True
                        })

                # for a questions just collect the answers
                else:

                    if catalog_entity.attribute_entity.id in values:

                        answers = []
                        for value in values[catalog_entity.attribute_entity.id]:

                            if value.option:
                                answers.append(value.option.text)
                            elif value.text:
                                answers.append(value.text)

                        if answers:
                            entities.append({
                                'text': catalog_entity.question.text,
                                'attribute': catalog_entity.attribute_entity.full_title,
                                'answers': answers,
                                'is_set': False
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
