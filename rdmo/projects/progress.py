from collections import defaultdict
from itertools import chain

from django.db.models import Exists, OuterRef, Q

from rdmo.conditions.models import Condition
from rdmo.core.utils import markdown2html
from rdmo.questions.models import Page, Question, QuestionSet


def get_catalog_conditions(catalog):
    pages_conditions_subquery = Page.objects.filter_by_catalog(catalog) \
                                            .filter(conditions=OuterRef('pk'))
    questionsets_conditions_subquery = QuestionSet.objects.filter_by_catalog(catalog) \
                                                          .filter(conditions=OuterRef('pk'))
    questions_conditions_subquery = Question.objects.filter_by_catalog(catalog) \
                                                    .filter(conditions=OuterRef('pk'))

    return Condition.objects.annotate(
        has_page=Exists(pages_conditions_subquery),
        has_questionset=Exists(questionsets_conditions_subquery),
        has_question=Exists(questions_conditions_subquery)
    ).filter(
        Q(has_page=True) | Q(has_questionset=True) | Q(has_question=True)
    ).distinct().select_related('source', 'target_option')


def resolve_conditions(catalog, values, sets):
    # resolve all conditions and return for each condition the set_prefix and set_index for which it resolved true
    conditions = defaultdict(set)
    if sets:
        for condition in get_catalog_conditions(catalog):
            conditions[condition.id] = {
                (set_prefix, set_index)
                for set_prefix, set_index in chain.from_iterable(sets.values())
                if condition.resolve(values, set_prefix=set_prefix, set_index=set_index)
            }

    return conditions


def compute_sets(values):
    # compute sets from values (including empty values)
    sets = defaultdict(set)
    for attribute, set_prefix, set_index in values.distinct_list():
        sets[attribute].add((set_prefix, set_index))
    return sets


def _visible_sets(element, conditions):
    """
    Return the set of (set_prefix, set_index) tuples for which *element*
    is visible according to its own conditions.

    Elements without a ``conditions`` manager (e.g. Catalog) are always
    visible in the root set ('', 0).
    """
    manager = getattr(element, 'conditions', None)
    if manager is None:
        return {('', 0)}

    element_conditions = {c.id for c in manager.all()}

    # no conditions → always visible
    if not element_conditions:
        return {('', 0)}

    is_collection = getattr(element, 'is_collection', False)
    visible = set()

    for condition_id in element_conditions:
        for set_prefix, set_index in conditions[condition_id]:
            if set_prefix == '':
                if is_collection:
                    visible.add(('', set_index))
                else:
                    visible.add(('', 0))
    return visible


def compute_next_relevant_page(current_page, direction, catalog, resolved_conditions):
    # recursively compute the next relevant page based on resolved conditions.
    # first, get the next page from the catalog based on the specified direction
    next_page = (
        catalog.get_prev_page(current_page) if direction == 'prev'
        else catalog.get_next_page(current_page)
    )

    # if there is no next page, return None
    if not next_page:
        return None

    # check if the next page meets the conditions
    if compute_show_page(next_page, resolved_conditions):
        return next_page

    # recursive step: check the next page
    return compute_next_relevant_page(next_page, direction, catalog, resolved_conditions)


def compute_show_page(page, conditions):
    # determine if a page should be shown based on resolved conditions
    # (show only pages with resolved conditions, but show all pages without conditions)
    return bool(_visible_sets(page, conditions))


def compute_navigation(section, project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # compute sets from values (including empty values)
    raw_sets = compute_sets(values)

    # resolve all conditions to get a dict mapping conditions to set_indexes
    conditions = resolve_conditions(project.catalog, values, raw_sets)

    # compute sets anew, but without empty optional values
    answered_sets = compute_sets(values.exclude_empty_optional(project.catalog))

    # query distinct, non empty set values
    answered_values = values.exclude_empty().distinct_list()

    navigation = []
    for catalog_section in project.catalog.elements:
        navigation_section = {
            'id': catalog_section.id,
            'uri': catalog_section.uri,
            'title': markdown2html(catalog_section.short_title or catalog_section.title),
            'first': catalog_section.elements[0].id if catalog_section.elements else None,
            'count': 0,
            'total': 0,
            'show': True  # will be adjusted later
        }
        if section is not None and catalog_section.id == section.id:
            navigation_section['pages'] = []

        for page in catalog_section.elements:
            # determine if a page should be shown or not
            show = compute_show_page(page, conditions)

            # count the total number of questions, taking sets and conditions into account
            counts = count_questions(page, answered_sets, conditions)

            # filter the answered_values for the attributes, and compute the total sum of counts
            count = sum(1 for value in answered_values if value[0] in counts)
            total = sum(counts.values())

            navigation_section['count'] += count
            navigation_section['total'] += total

            if 'pages' in navigation_section:
                navigation_section['pages'].append({
                    'id': page.id,
                    'uri': page.uri,
                    'title': markdown2html(page.short_title or page.title),
                    'show': show,
                    'count': count,
                    'total': total
                })

        # Hide or grey-out sections that contain no questions at all
        if navigation_section['total'] == 0:
            navigation_section['show'] = False

        navigation.append(navigation_section)

    return navigation


def compute_progress(project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # compute sets from values (including empty values), necessary for condition resolution
    raw_sets = compute_sets(values)

    # resolve all conditions
    conditions = resolve_conditions(project.catalog, values, raw_sets)

    # query distinct, non empty set values
    answered_values = values.exclude_empty().distinct_list()

    # compute sets anew, but without empty optional values
    answered_sets = compute_sets(values.exclude_empty_optional(project.catalog))

    # count the total number of questions, taking sets and conditions into account
    counts = count_questions(project.catalog, answered_sets, conditions)

    # filter the answered_values for the attributes, and compute the total sum of counts
    count = sum(1 for value in answered_values if value[0] in counts)
    total = sum(counts.values())

    return count, total


def count_questions(element, sets, conditions):
    """
    Recursively collect a mapping {attribute_id: required_answer_count}.

    * Pages / QuestionSets are considered only when *they themselves* are
      visible (their own conditions resolve).
    * Questions are counted only for the sets where *both* the parent element
      and the question are visible.
    """
    counts = defaultdict(int)

    # Skip elements that are completely hidden
    visible_sets = _visible_sets(element, conditions)
    if not visible_sets:
        return counts

    if isinstance(element, (Page, QuestionSet)):
        # obtain the maximum number of set-distinct values for the questions in this page or
        # question set. this number is how often each question is displayed and we will use
        # this number to determine how often a question needs to be counted
        element_sets = set()

        # a) own attribute values
        if element.attribute is not None:
            element_sets.update(sets[element.attribute.id])

        # b) direct child questions' attribute values
        for child in element.elements:
            if isinstance(child, Question) and child.attribute is not None:
                element_sets.update(sets[child.attribute.id])

        if element.is_collection:
            # count only those instances that are both answered and visible
            answered_visible_sets = element_sets & visible_sets
            set_count = len(answered_visible_sets)
            if set_count == 0:
                return counts
        else:
            set_count = 1
    else:
        # plain Question handled below
        set_count = 0


    for child in element.elements:
        if isinstance(child, Question):
            # honour the question's own conditions
            child_visible_sets = _visible_sets(child, conditions) & visible_sets
            if not child_visible_sets:
                continue

            if child.attribute is None:
                continue

            if child.is_optional:
                answered = len(sets[child.attribute.id] & child_visible_sets)
                counts[child.attribute.id] = max(counts[child.attribute.id], answered)
            else:
                counts[child.attribute.id] = max(counts[child.attribute.id],
                                                 len(child_visible_sets))
        else:
            # recurse into nested pages / questionsets
            counts.update(count_questions(child, sets, conditions))

    return counts
