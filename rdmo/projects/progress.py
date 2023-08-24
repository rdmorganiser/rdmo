from collections import defaultdict

from django.db.models import Exists, OuterRef, Q

from rdmo.conditions.models import Condition
from rdmo.questions.models import Catalog, Section, Page, QuestionSet, Question


def compute_progress(project, snapshot=None):
    # get all values for this project and snapshot
    project_values = project.values.filter(snapshot=snapshot).select_related('attribute', 'option')

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
        if condition.resolve(project_values):
            conditions.add(condition.id)

    # compute sets from values
    sets = defaultdict(list)
    for attribute, set_index in project_values.values_list('attribute', 'set_index').distinct():
        sets[attribute].append(set_index)

    # count the total number of questions, taking sets and conditions into account
    total_count, attributes = count_questions(project.catalog, sets, conditions)

    # filter the project values for the counted questions and exclude empty values
    values_count = project_values.filter(attribute__in=attributes) \
                                 .exclude((Q(text='') | Q(text=None)) & Q(option=None) &
                                          (Q(file='') | Q(file=None))) \
                                 .count()

    return values_count, total_count


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
                        attributes.append(element.attribute)
                        count += 1
                else:
                    if element.attribute:
                        attributes.append(element.attribute)

                    element_count, element_attributes = count_questions(element, sets, conditions)
                    set_count = count_sets(element, sets)
                    if set_count > 0:
                        count += element_count * set_count
                        attributes += element_attributes

    return count, attributes


def count_sets(parent_element, sets):
    if parent_element.is_collection:
        if parent_element.attribute:
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
