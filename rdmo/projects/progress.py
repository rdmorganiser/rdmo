from collections import defaultdict
from itertools import chain

from django.db.models import Exists, OuterRef, Q, prefetch_related_objects

from rdmo.conditions.models import Condition
from rdmo.core.utils import markdown2html
from rdmo.questions.models import Page, Question, QuestionSet

ROOT = ('', 0)


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


def _prefetch_tree_conditions(catalog):
    """
    Prefetch the M2M 'conditions' for all Page / QuestionSet / Question
    instances present in the in-memory catalog tree, so later calls to
    element.conditions.values_list(...) hit memory instead of the DB.
    """
    buckets = {Page: [], QuestionSet: [], Question: []}

    def walk(node):
        if isinstance(node, (Page, QuestionSet, Question)):
            buckets[type(node)].append(node)
        for ch in getattr(node, 'elements', []):
            walk(ch)

    for section in getattr(catalog, 'elements', []):
        for page in getattr(section, 'elements', []):
            walk(page)

    for model_cls, instances in buckets.items():
        if instances:
            prefetch_related_objects(instances, 'conditions')


def compute_condition_candidates(catalog, values):
    """
    Build the universe of (set_prefix, set_index) tuples that conditions may
    evaluate against by combining:

    1) Structure-first: always include the root ('', 0) so non-collection
       elements can become visible before any answers exist, and walk the
       catalog to add indices that are relevant for collection elements.
    2) Answers-second: include all set tuples that already exist in answers.
    """
    candidates = {ROOT}  # root must always exist for visibility of non-collections

    # Answer-derived sets (for all attributes)
    base_sets = compute_sets(values)  # {attribute_id -> {(set_prefix, set_index), ...}}
    candidates |= set(chain.from_iterable(base_sets.values()))

    # Walk the catalog to add collection-relevant indices derived from *existing* answers
    # (mirrors the frontend's structure-first mindset without inventing indices).
    def _collect_element_sets(element):
        # union of set tuples for element.attribute and immediate child questions
        union_sets = set()

        # a) own attribute
        if getattr(element, 'attribute', None) is not None:
            union_sets |= base_sets[element.attribute.id]

        # b) immediate child questions' attributes
        for child in getattr(element, 'elements', []):
            if isinstance(child, Question) and child.attribute is not None:
                union_sets |= base_sets[child.attribute.id]

        return union_sets

    def _walk(e):
        if isinstance(e, (Page, QuestionSet)) and e.is_collection:
            # add indices that *exist in answers* for this element scope
            candidates.update(_collect_element_sets(e))
        for ch in getattr(e, 'elements', []):
            _walk(ch)

    for section in catalog.elements:
        for page in section.elements:
            _walk(page)

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
    page_condition_ids = set(page.conditions.values_list('id', flat=True))
    if page_condition_ids:
        # check if any valuesets for set_prefix = '' resolved
        # for non collection pages restrict further to set_index = 0
        for cond_id in page_condition_ids:
            for set_prefix, set_index in conditions[cond_id]:
                if (set_prefix == '') and (page.is_collection or set_index == 0):
                    return True
        return False
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
        return {ROOT}

    # no conditions → visible at the root
    element_condition_ids = set(element.conditions.values_list('id', flat=True))
    if not element_condition_ids:
        return {ROOT}

    is_collection = getattr(element, 'is_collection', False)
    visible = set()

    for cond_id in element_condition_ids:
        for set_prefix, set_index in conditions[cond_id]:
            if set_prefix == '':
                if is_collection:
                    visible.add(('', set_index))
                else:
                    visible.add(ROOT)
    return visible


def compute_navigation(section, project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # prefetch 'conditions' for the whole tree to avoid per-node queries
    _prefetch_tree_conditions(project.catalog)

    # structure-first candidates (root + answer-derived indices + catalog walk)
    condition_candidates = compute_condition_candidates(project.catalog, values)

    # resolve all conditions to get a dict mapping conditions to set_indexes
    conditions = resolve_conditions(project.catalog, values, condition_candidates)

    # compute sets anew, but without empty optional values
    sets = compute_sets(values.exclude_empty_optional(project.catalog))

    # query distinct, non empty set values
    values_list = values.exclude_empty().distinct_list()
    _answered_attr_ids = {attr_id for (attr_id, _, _) in values_list}

    navigation = []
    for catalog_section in project.catalog.elements:
        navigation_section = {
            'id': catalog_section.id,
            'uri': catalog_section.uri,
            'title': markdown2html(catalog_section.short_title or catalog_section.title),
            'first': catalog_section.elements[0].id if catalog_section.elements else None,
            'count': 0,   # will be recomputed below
            'total': 0,   # will be recomputed below
            'show': True  # hide/grey-out when the section has no questions at all
        }
        if section is not None and catalog_section.id == section.id:
            navigation_section['pages'] = []

        # aggregate per-section using max per attribute (mirrors compute_progress)
        section_counts = defaultdict(int)

        for page in catalog_section.elements:

            # determine if a page should be shown or not
            show = compute_show_page(page, conditions)

            # count the total number of questions, taking sets and conditions into account
            page_counts = count_questions(page, sets, conditions)

            # keep page-level numbers unchanged for the UI
            page_total = sum(page_counts.values())
            # page count per *value instance*, not per attribute
            page_count = sum(1 for (attr_id, _, _) in values_list if attr_id in page_counts)
            # alternatively, the values could be deduplicated for attr id
            _unique_attr_page_count = len(set(page_counts).intersection(_answered_attr_ids))

            if 'pages' in navigation_section:
                navigation_section['pages'].append({
                    'id': page.id,
                    'uri': page.uri,
                    'title': markdown2html(page.short_title or page.title),
                    'show': show,
                    'count': page_count,
                    'total': page_total
                })

            # merge page_counts into section_counts using max per attribute
            for attr_id, needed in page_counts.items():
                if needed > section_counts[attr_id]:
                    section_counts[attr_id] = needed

        # compute section totals from the aggregated dict (prevents double-counting)
        navigation_section['total'] = sum(section_counts.values())
        # section count must be per *value instance*
        navigation_section['count'] = sum(1 for (attr_id, _, _) in values_list if attr_id in section_counts)
        # alternatively, the section count could be deduplicated for attr id
        _unique_section_count = len(set(section_counts).intersection(_answered_attr_ids))

        # hide / grey-out sections which contain no questions at all
        if navigation_section['total'] == 0:
            navigation_section['show'] = False

        navigation.append(navigation_section)

    return navigation


def compute_progress(project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # prefetch 'conditions' for the whole tree to avoid per-node queries
    _prefetch_tree_conditions(project.catalog)

    # structure-first candidates (root + answer-derived indices + catalog walk)
    condition_candidates = compute_condition_candidates(project.catalog, values)

    # resolve all conditions to get a dict mapping conditions to set_indexes
    conditions = resolve_conditions(project.catalog, values, condition_candidates)

    # query distinct, non empty set values
    values_list = values.exclude_empty().distinct_list()  # [(attr_id, set_prefix, set_index), ...]
    _answered_attr_ids = {attr_id for (attr_id, _, _) in values_list}

    # compute sets anew, but without empty optional values
    sets = compute_sets(values.exclude_empty_optional(project.catalog))

    # count the total number of questions, taking sets and conditions into account
    counts = count_questions(project.catalog, sets, conditions)  # {attr_id: required_instances}

    # filter the values_list for the attributes, and compute the total sum of counts
    _unique_attribute_count = len(set(counts).intersection(_answered_attr_ids))
    # overall count per *value instance* across the whole catalog
    count = sum(1 for (attr_id, _, _) in values_list if attr_id in counts)
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
            element_sets |= sets[element.attribute.id]

        # count the sets for the questions in the page or question
        for child in element.elements:
            if isinstance(child, Question) and child.attribute is not None:
                element_sets |= sets[child.attribute.id]

        # look for the elements conditions
        element_condition_ids = set(element.conditions.values_list('id', flat=True))

        # if this element has conditions: check if those conditions resolve for the found sets
        if element_condition_ids:
            element_condition_intersection = set().union(*(conditions[cid] for cid in element_condition_ids))
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
            child_condition_ids = set(child.conditions.values_list('id', flat=True))
        else:
            child_condition_ids = set()

        # compute the intersection of the conditions of this child with the full set of conditions
        child_condition_intersection = set().union(
            *(conditions[cid] for cid in child_condition_ids)
        ) if child_condition_ids else set()

        # check if the element either has no condition or its conditions intersect with the full set of conditions
        if not child_condition_ids or child_condition_intersection:
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
                                element_sets.intersection(child_condition_intersection)
                                if child_condition_intersection else element_sets
                            )
                        else:
                            parent_visible_sets = (
                                {ROOT} if (
                                        not child_condition_ids or
                                        any(sp == '' for sp, _ in child_condition_intersection)
                                ) else set()
                            )

                        child_count = len(sets[child.attribute.id].intersection(parent_visible_sets))
                        counts[child.attribute.id] = max(counts[child.attribute.id], child_count)
                    else:
                        if child_condition_ids:
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
