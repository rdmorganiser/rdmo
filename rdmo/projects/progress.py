from collections import defaultdict

from django.db.models import Exists, OuterRef, Q

from rdmo.conditions.models import Condition
from rdmo.questions.models import Page, Question, QuestionSet


def resolve_conditions(project, values):
    # get all conditions for this catalog
    pages_conditions_subquery = Page.objects.filter_by_catalog(project.catalog) \
                                            .filter(conditions=OuterRef('pk'))
    questionsets_conditions_subquery = QuestionSet.objects.filter_by_catalog(project.catalog) \
                                                          .filter(conditions=OuterRef('pk'))
    questions_conditions_subquery = Question.objects.filter_by_catalog(project.catalog) \
                                                    .filter(conditions=OuterRef('pk'))

    catalog_conditions = Condition.objects.annotate(has_page=Exists(pages_conditions_subquery)) \
                                          .annotate(has_questionset=Exists(questionsets_conditions_subquery)) \
                                          .annotate(has_question=Exists(questions_conditions_subquery)) \
                                          .filter(Q(has_page=True) | Q(has_questionset=True) | Q(has_question=True)) \
                                          .distinct().select_related('source', 'target_option')

    # evaluate conditions
    conditions = set()
    for condition in catalog_conditions:
        if condition.resolve(values):
            conditions.add(condition.id)

    # return all true conditions for this project
    return conditions


def compute_navigation(section, project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # get true conditions
    conditions = resolve_conditions(project, values)

    # compute sets from values (including empty values)
    sets = defaultdict(lambda: defaultdict(list))
    for attribute, set_prefix, set_index in values.distinct_list():
        sets[attribute][set_prefix].append(set_index)

    # query distinct, non empty set values
    values_list = values.exclude_empty().distinct_list()

    navigation = []
    for catalog_section in project.catalog.elements:
        navigation_section = {
            'id': catalog_section.id,
            'uri': catalog_section.uri,
            'title': catalog_section.title,
            'first': catalog_section.elements[0].id if section.elements else None
        }
        if catalog_section.id == section.id:
            navigation_section['pages'] = []
            for page in catalog_section.elements:
                pages_conditions = {page.id for page in page.conditions.all()}
                show = bool(not pages_conditions or pages_conditions.intersection(conditions))

                # count the total number of questions, taking sets and conditions into account
                counts = count_questions(page, sets, conditions)

                # filter the values_list for the attributes, and compute the total sum of counts
                count = len(tuple(filter(lambda value: value[0] in counts.keys(), values_list)))
                total = sum(counts.values())

                navigation_section['pages'].append({
                    'id': page.id,
                    'uri': page.uri,
                    'title': page.title,
                    'show': show,
                    'count': count,
                    'total': total
                })

        navigation.append(navigation_section)

    return navigation


def compute_progress(project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # get true conditions
    conditions = resolve_conditions(project, values)

    # compute sets from values (including empty values)
    sets = defaultdict(lambda: defaultdict(list))
    for attribute, set_prefix, set_index in values.distinct_list():
        sets[attribute][set_prefix].append(set_index)

    # query distinct, non empty set values
    values_list = values.exclude_empty().distinct_list()


    # count the total number of questions, taking sets and conditions into account
    counts = count_questions(project.catalog, sets, conditions)

    # filter the values_list for the attributes, and compute the total sum of counts
    count = len(tuple(filter(lambda value: value[0] in counts.keys(), values_list)))
    total = sum(counts.values())

    return count, total


def count_questions(element, sets, conditions):
    counts = defaultdict(int)

    # obtain the maximum number of set-distinct values the questions in this element
    # this number is how often each question is displayed and we will use this number
    # to determine how often a question needs to be counted
    if isinstance(element, (Page, QuestionSet)) and element.is_collection:
        set_count = 0

        if element.attribute is not None:
            child_count = sum(len(set_indexes) for set_indexes in sets[element.attribute.id].values())
            set_count = max(set_count, child_count)

        for child in element.elements:
            if isinstance(child, Question):
                child_count = sum(len(set_indexes) for set_indexes in sets[child.attribute.id].values())
                set_count = max(set_count, child_count)
    else:
        set_count = 1

    # loop over all children of this element
    for child in element.elements:
        # look for the elements conditions
        if isinstance(child, (Page, QuestionSet, Question)):
            child_conditions = {condition.id for condition in child.conditions.all()}
        else:
            child_conditions = []

        if not child_conditions or child_conditions.intersection(conditions):
            if isinstance(child, Question):
                # for questions add the set_count to the counts dict
                # use the max function, since the same attribute could apear twice in the tree
                if child.attribute is not None and not child.is_optional:
                    counts[child.attribute.id] = max(counts[child.attribute.id], set_count)
            else:
                # for everthing else, call this function recursively
                counts.update(count_questions(child, sets, conditions))

    return counts
