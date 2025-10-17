from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import Any

from rdmo.core.utils import markdown2html
from rdmo.projects.answers.conditions import ConditionEvaluator
from rdmo.projects.answers.set import SetAddr
from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section


@dataclass
class AnswerTree:

    catalog: Catalog
    values: Any

    @cached_property
    def sets(self):
        sets = defaultdict(set)
        for attribute, set_prefix, set_index in self.values.distinct_list():
            sets[attribute].add(SetAddr.from_db(set_prefix, set_index))
        return sets

    @cached_property
    def conditions_evaluator(self):
        return ConditionEvaluator(self.catalog.conditions, self.values)

    def compute(self):
        # Main function of this class, which Computes the answer tree recursively.
        # First, it computes the catalog, section, and page nodes.
        # Then, it alternates between (value)set and questionset nodes until it reaches
        # the question nodes, which include the corresponding values as well as how much
        # this question counts to the count and total values for the progress.
        return self.compute_element_node(self.catalog)

    def compute_element_node(self, element, parent_set: SetAddr | None=None):
        # recursive function, which will be called for each element
        element_node = {
            'id': element.id,
            'uri': element.uri,
            'model': str(element._meta),
            'show': True
        }

        if isinstance(element, (Section, Page)):
            element_node['title'] = markdown2html(element.short_title or element.title)

        if isinstance(element, (Page, QuestionSet, Question)):
            if element.has_conditions:
                # for pages, questionsets and questions evaluate conditions
                result, triggers = self.conditions_evaluator.resolve_for_element(element, parent_set)

                # if the element is not shown, break the recursion
                if not result:
                    element_node.update({
                        'show': False,
                        'count': 0,
                        'total': 0,
                        'hidden_due_to': triggers,
                    })
                    return element_node
                else:
                    element_node['shown_due_to'] = triggers

        if isinstance(element, (Catalog, Section)):
            # for catalogs and sections we recurse to the next level of elements (sections, pages)
            element_node['elements'] = [
                self.compute_element_node(child_element)
                for child_element in element.elements
            ]

            # find the first element
            element_node['first'] = element_node['elements'][0]['id']

            # aggregate count and total from the child elements
            element_node['count'] = sum(child_node['count'] for child_node in element_node['elements'])
            element_node['total'] = sum(child_node['total'] for child_node in element_node['elements'])

        elif isinstance(element, (Page, QuestionSet)):
            # for pages and questionsets we first compute the sets for the element ...
            element_sets = self.compute_element_sets(element, parent_set)  # -> list[SetAddr]

            # ... and then create a set node for each set (the recursion continues in compute_set_node)
            element_node['sets'] = [
                self.compute_set_node(element, element_set)
                for element_set in element_sets
            ]

            # aggregate count and total from the set nodes
            element_node['count'] = sum(set_node['count'] for set_node in element_node['sets'])
            element_node['total'] = sum(set_node['total'] for set_node in element_node['sets'])

        elif isinstance(element, Question):
            # for questions we add the text and the values and compute if this question
            # can be considered empty, meaning it has no or only empty values
            element_node['text'] = element.text
            element_node['values'] = self.compute_element_values(element, parent_set)
            element_node['is_empty'] = all(value['is_empty'] for value in element_node['values'])

            # the question only counts for the progress if is not considered empty
            element_node['count'] = 1 if not element_node['is_empty'] else 0

            # whether the question counts for the total number depends on if it is optional
            if element.is_optional:
                # optional questions only count if they are not empty
                element_node['total'] = 1 if not element_node['is_empty'] else 0
            else:
                # regular questions count if they have any values
                element_node['total'] = 1 if element_node['values'] else 0

        return element_node

    def compute_set_node(self, element, element_set: SetAddr):
        # recursive function, which will be called for each set in pages and questionsets
        set_node = {
            'set_prefix': element_set.set_prefix,
            'set_index': element_set.set_index,
            'elements': [  # compute the next level of nodes
                self.compute_element_node(child_element, parent_set=element_set)
                for child_element in element.elements
        ]}

        # aggregate count and total from the element nodes
        set_node['count'] = sum(element_node['count'] for element_node in set_node['elements'])
        set_node['total'] = sum(element_node['total'] for element_node in set_node['elements'])

        return set_node

    def compute_element_sets(self, element, parent_set: SetAddr | None) -> list[SetAddr]:
        # computes the required sets for each page/questionset
        element_sets: set[SetAddr] = set()

        # compute the level in the page/questionsets hierarchy
        level = 0 if parent_set is None else parent_set.prefix.parent_level

        # for pages, add the sets for the attribute of the page (root only)
        if parent_set is None and element.attribute:
            for set_addr in self.sets[element.attribute.id]:
                if set_addr.prefix.is_root:  # only include sets for pages (root prefix)
                    element_sets.add(SetAddr.from_db('', set_addr.set_index))

        # full parent path (prefix + index)
        parent_full_prefix = parent_set.as_child_prefix() if parent_set else None

        # for each descendant find the sets and add the set for this element, which is
        # needed to "reach" the descendant set
        for descendant in element.descendants:
            if descendant.attribute is None:
                continue
            if descendant.attribute.id not in self.sets:
                continue

            if parent_full_prefix is None:
                descendant_sets = self.sets[descendant.attribute.id]
            else:
                descendant_sets = {
                    addr for addr in self.sets[descendant.attribute.id]
                    if addr.prefix.is_descendant_of(parent_full_prefix, include_self=True)
                }

            if descendant in element.elements:
                # for the direct children (i.e. questions), we add just the sets
                element_sets.update(descendant_sets)
            else:
                # for the other descendants (i.e. questions in questionsets), we need
                # to split the set_prefix according to the level we are in
                for set_addr in descendant_sets:
                    # exclude sets with an empty set_prefix (misconfigured catalogs)
                    if set_addr.prefix.is_root:
                        continue
                    if child := set_addr.child_at_level(level):
                        element_sets.add(child)

        # create one empty set for non-collection pages/questionsets
        if not element.is_collection:
            element_sets.add(SetAddr.branch_under(parent_set))

        # stable ordering for deterministic output
        return sorted(element_sets)

    def compute_element_values(self, element, parent_set: SetAddr):
        # filter the values for this element and set
        if element_values := [
                {
                    'id': value.id,
                    'is_empty': value.is_empty,
                    'collection_index': value.collection_index,
                }
                for value in self.values
                if value.attribute == element.attribute
                and value.set_prefix == parent_set.set_prefix
                and value.set_index == parent_set.set_index
            ]:
            # if there are values, return them
            return element_values
        # If no values are present:
        if element.is_optional:  # * For optional questions, return an empty list.
            return []
        return [  # * For required questions, return a placeholder dict.
            {
                'is_empty': True,
                'collection_index': 0
            }
        ]
