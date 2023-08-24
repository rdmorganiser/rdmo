from collections import defaultdict

from django.db.models import Exists, OuterRef, Q

from rdmo.conditions.models import Condition
from rdmo.questions.models import Catalog, Section, Page, QuestionSet, Question


def resolve_conditions(project, values):
    # get all conditions for this catalog
    pages_conditions_subquery = Page.objects.filter_by_catalog(project.catalog).filter(conditions=OuterRef('pk'))
    questionsets_conditions_subquery = QuestionSet.objects.filter_by_catalog(project.catalog).filter(conditions=OuterRef('pk'))
    questions_conditions_subquery = Question.objects.filter_by_catalog(project.catalog).filter(conditions=OuterRef('pk'))

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


def compute_sets(values):
    sets = defaultdict(list)
    for attribute, set_index in values.values_list('attribute', 'set_index').distinct():
        sets[attribute].append(set_index)
    return sets


def compute_navigation(section, project, snapshot=None):
    # get all values for this project and snapshot
    values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

    # get true conditions
    conditions = resolve_conditions(project, values)

    # compute sets from values
    sets = compute_sets(values)

    # query non empty values
    values_list = values.exclude((Q(text='') | Q(text=None)) & Q(option=None) &
                                 (Q(file='') | Q(file=None))) \
                        .values_list('attribute', 'set_index').distinct() \
                        .values_list('attribute', flat=True)

    navigation = []
    for catalog_section in project.catalog.elements:
        navigation_section = {
            'id': catalog_section.id,
            'title': catalog_section.title,
            'first': catalog_section.elements[0].id if section.elements else None
        }
        if catalog_section.id == section.id:
            navigation_section['pages'] = []
            for page in catalog_section.elements:
                pages_conditions = set(page.id for page in page.conditions.all())
                show = bool(not pages_conditions or pages_conditions.intersection(conditions))

                # count the total number of questions, taking sets and conditions into account
                total, attributes = count_questions(page, sets, conditions)

                # filter the project values for the counted questions and exclude empty values
                count = len(tuple(filter(lambda attribute: attribute in attributes, values_list)))

                navigation_section['pages'].append({
                    'id': page.id,
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

    # compute sets from values
    sets = compute_sets(values)

    # count the total number of questions, taking sets and conditions into account
    total, attributes = count_questions(project.catalog, sets, conditions)

    # filter the project values for the counted questions and exclude empty values
    count = values.filter(attribute_id__in=attributes) \
                  .exclude((Q(text='') | Q(text=None)) & Q(option=None) &
                           (Q(file='') | Q(file=None))) \
                  .values_list('attribute', 'set_index').distinct().count()

    return count, total


def count_questions(parent_element, sets, conditions):
    count = 0
    attributes = []

    for element in parent_element.elements:
        if isinstance(element, (Catalog, Section)):
            element_count, element_attributes = count_questions(element, sets, conditions)
            attributes += element_attributes
            count += element_count
        else:
            element_conditions = set(condition.id for condition in element.conditions.all())
            if not element_conditions or element_conditions.intersection(conditions):
                if isinstance(element, Question):
                    if not element.is_optional:
                        attributes.append(element.attribute_id)
                        count += 1
                else:
                    if element.attribute_id:
                        attributes.append(element.attribute_id)

                    element_count, element_attributes = count_questions(element, sets, conditions)
                    set_count = count_sets(element, sets)
                    if set_count > 0:
                        count += element_count * set_count
                        attributes += element_attributes

    return count, attributes


def count_sets(parent_element, sets):
    if parent_element.is_collection:
        if parent_element.attribute_id:
            count = len(sets[parent_element.attribute_id])
        else:
            count = 0
    else:
        count = 1

    for element in parent_element.elements:
        if isinstance(element, Question):
            element_count = len(sets[element.attribute_id])
            if element_count > count:
                count = element_count

    return count
