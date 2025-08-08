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


def compute_condition_candidates(values):
    """
    Build the universe of (set_prefix, set_index) tuples that conditions may
    evaluate against.

    Always include the root ('', 0) so non-collection elements can become
    visible before any answers exist, and include all set tuples that already
    exist in answers.
    """
    candidates = {('', 0)}
    base_sets = compute_sets(values)
    if base_sets:
        candidates |= set(chain.from_iterable(base_sets.values()))
    return candidates


def resolve_conditions(catalog, values, condition_candidates):
    # resolve all conditions and return for each condition the set_prefix and set_index for which it resolved true
    conditions = defaultdict(set)
    for condition in get_catalog_conditions(catalog):
        conditions[condition.id] = {
            (set_prefix, set_index)
            for (set_prefix, set_index) in condition_candidates
            if condition.resolve(values, set_prefix=set_prefix, set_index=set_index)
        }
    return conditions


def compute_sets(values):
    # compute sets from values (including empty values)
    sets = defaultdict(set)
    for attribute, set_prefix, set_index in values.distinct_list():
        sets[attribute].add((set_prefix, set_index))
    return sets


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
    # show only pages with resolved conditions, but show all pages without conditions
    pages_conditions = {page.id for page in page.conditions.all()}

    if pages_conditions:
        # check if any valuesets for set_prefix = '' resolved
        # for non collection pages restrict further to set_index = 0

        return any(
            (set_prefix == '') and (page.is_collection or set_index == 0)
            for page_condition in pages_conditions
            for set_prefix, set_index in conditions[page_condition]
        )
    else:
        return True


def _visible_sets(element, conditions):
    """
    Return the set of (set_prefix, set_index) tuples for which *element*
    is visible according to its own conditions.

    Only Page, QuestionSet, and Question have conditions; all other types
    are treated as visible in the root set ('', 0).
    """
    if not isinstance(element, (Page, QuestionSet, Question)):
        return {('', 0)}

    element_conditions = {c.id for c in element.conditions.all()}

    # no conditions → visible at the root
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


def compute_navigation(section, project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # build condition candidates (root + answered instances)
    condition_candidates = compute_condition_candidates(values)

    # resolve all conditions to get a dict mapping conditions to set_indexes
    conditions = resolve_conditions(project.catalog, values, condition_candidates)

    # compute sets anew, but without empty optional values
    sets = compute_sets(values.exclude_empty_optional(project.catalog))

    # query distinct, non empty set values
    values_list = values.exclude_empty().distinct_list()

    navigation = []
    for catalog_section in project.catalog.elements:
        navigation_section = {
            'id': catalog_section.id,
            'uri': catalog_section.uri,
            'title': markdown2html(catalog_section.short_title or catalog_section.title),
            'first': catalog_section.elements[0].id if catalog_section.elements else None,
            'count': 0,
            'total': 0,
            'show': True  # hide/grey-out when the section has no questions at all
        }
        if section is not None and catalog_section.id == section.id:
            navigation_section['pages'] = []

        for page in catalog_section.elements:

            # determine if a page should be shown or not
            show = compute_show_page(page, conditions)

            # count the total number of questions, taking sets and conditions into account
            counts = count_questions(page, sets, conditions)

            # filter the values_list for the attributes, and compute the total sum of counts
            count = sum(1 for value in values_list if value[0] in counts)
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

        # hide / grey-out sections which contain no questions at all
        if navigation_section['total'] == 0:
            navigation_section['show'] = False

        navigation.append(navigation_section)

    return navigation


def compute_progress(project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # build condition candidates (root + answered instances)
    condition_candidates = compute_condition_candidates(values)

    # resolve all conditions to get a dict mapping conditions to set_indexes
    conditions = resolve_conditions(project.catalog, values, condition_candidates)

    # query distinct, non empty set values
    values_list = values.exclude_empty().distinct_list()

    # compute sets anew, but without empty optional values
    sets = compute_sets(values.exclude_empty_optional(project.catalog))

    # count the total number of questions, taking sets and conditions into account
    counts = count_questions(project.catalog, sets, conditions)

    # filter the values_list for the attributes, and compute the total sum of counts
    count = sum(1 for value in values_list if value[0] in counts)
    total = sum(counts.values())

    return count, total


def count_questions(element, sets, conditions):
    counts = defaultdict(int)

    # Skip elements that are completely hidden (only Page/QuestionSet can be hidden)
    if isinstance(element, (Page, QuestionSet)) and not compute_show_page(element, conditions):
        return counts

    if isinstance(element, (Page, QuestionSet)):
        # obtain the maximum number of set-distinct values for the questions in this page or
        # question set. this number is how often each question is displayed and we will use
        # this number to determine how often a question needs to be counted
        element_sets = set()

        # count the sets for the id attribute of the page or question
        if element.attribute is not None:
            # nested loop over the separate set_prefix, set_index lists in sets[element.attribute.id]
            for set_prefix, set_index in sets[element.attribute.id]:
                element_sets.add((set_prefix, set_index))

        # count the sets for the questions in the page or question
        for child in element.elements:
            if isinstance(child, Question):
                if child.attribute is not None:
                    # nested loop over the separate set_prefix, set_index lists in sets[element.attribute.id]
                    for set_prefix, set_index in sets[child.attribute.id]:
                        element_sets.add((set_prefix, set_index))

        # look for the elements conditions
        element_conditions = {condition.id for condition in element.conditions.all()}

        # if this element has conditions: check if those conditions resolve for the found sets
        if element_conditions:
            # compute the intersection of the conditions of this child with the full set of conditions
            element_condition_intersection = {
                (set_prefix, set_index)
                for condition_id in element_conditions
                for set_prefix, set_index in conditions[condition_id]
            }

            resolved_sets = element_sets.intersection(element_condition_intersection)

            # collections: count answered & visible instances only; non-collections: count once when visible
            if element.is_collection:
                if resolved_sets:
                    set_count = len(resolved_sets)
                else:
                    # return immediately and do not consider children, this page/questionset is hidden
                    return counts
            else:
                # non-collection elements: visibility is enough to count once
                is_visible = bool(_visible_sets(element, conditions))  # root ('', 0)
                if not is_visible:
                    return counts
                set_count = 1
        else:
            # no conditions on the element:
            # - collections rely on answered sets
            # - non-collections count once
            set_count = len(element_sets) if element.is_collection else 1

    # loop over all children of this element
    for child in element.elements:
        # look for the child element's conditions (only for Page/QuestionSet/Question)
        if isinstance(child, (Page, QuestionSet, Question)):
            child_conditions = {condition.id for condition in child.conditions.all()}
        else:
            child_conditions = set()

        # compute the intersection of the conditions of this child with the full set of conditions
        child_condition_intersection = {
            (set_prefix, set_index)
            for condition_id in child_conditions
            for set_prefix, set_index in conditions[condition_id]
        }

        # check if the element either has no condition or its conditions intersect with the full set of conditions
        if not child_conditions or child_condition_intersection:
            if isinstance(child, Question):
                # for regular questions add the set_count to the counts dict, since the
                # question should be answered in every set
                # for optional questions add just the number of present answers, so that
                # only answered questions count for the progress/navigation
                # use the max function, since the same attribute could appear twice in the tree
                if child.attribute is not None:
                    if child.is_optional:
                        # only answered optional questions count; restrict to visible sets
                        # parent non-collection → root only; collection → intersection with visible instances
                        if isinstance(element, (Page, QuestionSet)) and element.is_collection:
                            parent_visible_sets = (
                                element_sets.intersection(child_condition_intersection) if
                                child_conditions else element_sets
                            )
                        else:
                            parent_visible_sets = (
                                {('', 0)} if (
                                        not child_conditions or any(sp == '' for sp, _ in child_condition_intersection)
                                ) else set())

                        child_count = len(sets[child.attribute.id].intersection(parent_visible_sets))
                        counts[child.attribute.id] = max(counts[child.attribute.id], child_count)
                    else:
                        if child_conditions:
                            if isinstance(element, (Page, QuestionSet)) and element.is_collection:
                                # only those instances of the collection where the question is visible
                                current_count = len(element_sets.intersection(child_condition_intersection))
                            else:
                                # non-collection parent → if question visible at root, count once
                                current_count = 1 if any(sp == '' for sp, _ in child_condition_intersection) else 0
                        else:
                            current_count = set_count

                        counts[child.attribute.id] = max(counts[child.attribute.id], current_count)
            else:
                # for everything else, call this function recursively
                counts.update(count_questions(child, sets, conditions))

    return counts
