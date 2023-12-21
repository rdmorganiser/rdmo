from collections import defaultdict
from itertools import chain

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

    # obtain the maximum number of set-distinct values for the questions in this page or
    # question set this number is how often each question is displayed and we will use
    # this number to determine how often a question needs to be counted
    if isinstance(element, (Page, QuestionSet)) and element.is_collection:
        counted_sets = set()

        # count the sets for the id attribute of the page or question
        if element.attribute is not None:
            # nested loop over the seperate set_index lists in sets[element.attribute.id]
            for set_index in chain.from_iterable(sets[element.attribute.id].values()):
                counted_sets.add(set_index)

        # count the sets for the questions in the page or question
        for child in element.elements:
            if isinstance(child, Question):
                if child.attribute is not None:
                    # nested loop over the seperate set_index lists in sets[element.attribute.id]
                    for set_index in chain.from_iterable(sets[child.attribute.id].values()):
                        counted_sets.add(set_index)

        set_count = len(counted_sets)
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
                # for regular questions add the set_count to the counts dict, since the
                # question should be answered in every set
                # for optional questions add just the number of present answers, so that
                # only answered questions count for the progress/navigation
                # use the max function, since the same attribute could apear twice in the tree
                if child.attribute is not None:
                    if child.is_optional:
                        child_count = sum(len(set_indexes) for set_indexes in sets[child.attribute.id].values())
                        counts[child.attribute.id] = max(counts[child.attribute.id], child_count)
                    else:
                        counts[child.attribute.id] = max(counts[child.attribute.id], set_count)
            else:
                # for everthing else, call this function recursively
                counts.update(count_questions(child, sets, conditions))

    return counts
