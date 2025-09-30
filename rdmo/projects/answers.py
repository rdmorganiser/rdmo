from collections import defaultdict

from django.db.models import Exists, OuterRef, Q
from django.utils.functional import cached_property

from rdmo.conditions.models import Condition
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section


class AnswerTree:

    def __init__(self, project, snapshot=None):
        self.project = project
        self.snapshot = snapshot

    @cached_property
    def conditions(self):
        pages_conditions_subquery = Page.objects.filter_by_catalog(self.project.catalog) \
                                                .filter(conditions=OuterRef('pk'))
        questionsets_conditions_subquery = QuestionSet.objects.filter_by_catalog(self.project.catalog) \
                                                              .filter(conditions=OuterRef('pk'))
        questions_conditions_subquery = Question.objects.filter_by_catalog(self.project.catalog) \
                                                        .filter(conditions=OuterRef('pk'))

        return Condition.objects.annotate(
            has_page=Exists(pages_conditions_subquery),
            has_questionset=Exists(questionsets_conditions_subquery),
            has_question=Exists(questions_conditions_subquery)
        ).filter(
            Q(has_page=True) | Q(has_questionset=True) | Q(has_question=True)
        ).distinct().select_related('source', 'target_option')

    @cached_property
    def values(self):
        return self.project.values.filter(snapshot=self.snapshot).select_related('attribute', 'option')

    @cached_property
    def sets(self):
        sets = defaultdict(set)
        for attribute, set_prefix, set_index in self.values.distinct_list():
            sets[attribute].add((set_prefix, set_index))
        return sets

    def compute(self):
        return self.compute_element_node(self.project.catalog)

    def compute_element_node(self, element, parent_set=None):
        # main recursive function of this class, which will be called for each element and for each set
        element_node = {
            'id': element.id,
            'uri': element.uri,
            'model': str(element._meta)
        }

        if isinstance(element, (Catalog, Section)):
            # for catalogs and sections we just compute the next level of nodes
            element_node['elements'] = [
                self.compute_element_node(child_element)
                for child_element in element.elements
            ]

        elif isinstance(element, (Page, QuestionSet)):
            # for pages and questionsets we first compute the sets for the element ...
            element_sets = self.compute_element_sets(element, parent_set)

            # ... and then create a set node for each set
            element_node['sets'] = [
                self.compute_set_node(element, element_set)
                for element_set in element_sets
            ]

        elif isinstance(element, Question):
            # for questions we just add the text and the values (for the parent set)
            element_node['text'] = element.text
            element_node['values'] = self.compute_element_values(element, parent_set)

        return element_node

    def compute_set_node(self, element, element_set):
        # recursive function, which will be called for each set in pages and questionsets
        set_prefix, set_index = element_set

        set_node = {
            'set_prefix': set_prefix,
            'set_index': set_index
        }

        # compute the next level of nodes
        set_node['elements'] = [
            self.compute_element_node(child_element, element_set)
            for child_element in element.elements
        ]

        return set_node

    def compute_element_sets(self, element, parent_set):
        # computes the required sets for each page/questionset
        element_sets = set()

        # compute the level in the page/questionsets hierarchy
        level = 0 if not parent_set else parent_set[0].count('|') + 1

        # if the element has an attribute (e.g. a page), add the sets for this attribute
        if element.attribute and element.attribute.id in self.sets:
            element_sets.update(self.sets[element.attribute.id])

        # for each descendant find the sets and add the set for this element, which is
        # needed to "reach" the descendant set
        for descendant in element.descendants:
            if descendant.attribute and descendant.attribute.id in self.sets:
                descendant_sets = self.sets[descendant.attribute.id]

                if descendant in element.elements:
                    # for the direct children (i.e. questions), we add just the sets
                    element_sets.update(descendant_sets)
                else:
                    # for the other descendants (i.e. questions in questionsets), we need
                    # to split the set_prefix according to the level we are in
                    for descendant_set_prefix, _ in descendant_sets:
                        descendant_set_prefix_split = descendant_set_prefix.split('|')

                        if level:
                            element_set = (
                                '|'.join(descendant_set_prefix_split[:level]),
                                int(descendant_set_prefix_split[level])
                            )
                        else:
                            element_set = ('', int(descendant_set_prefix_split[0]))

                        element_sets.add(element_set)

        # create one empty set for non-collection pages/questionsets
        if not element.is_collection:
            if parent_set is None:
                element_sets.add(('', 0))
            else:
                parent_set_prefix, parent_set_index = parent_set
                set_prefix = f'{parent_set_prefix}|{parent_set_index}' if parent_set_prefix else str(parent_set_index)
                element_sets.add((set_prefix, 0))

        return element_sets

    def compute_element_values(self, element, parent_set):
        set_prefix, set_index = parent_set

        element_values = list(filter(lambda v: all((
            v.attribute == element.attribute,
            v.set_prefix == set_prefix,
            v.set_index == set_index,
        )), self.values))

        if element_values:
            return [
                {
                    'id': value.id,
                    'is_empty': value.is_empty,
                    'collection_index': value.collection_index
                }
                for value in element_values
            ]
        elif not element.is_collection:
            # create one empty set for non-collection questions
            return [
                {
                    'is_empty': True,
                    'collection_index': 0
                }
            ]
        else:
            return []
