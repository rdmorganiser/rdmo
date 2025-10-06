from collections import defaultdict

from django.utils.functional import cached_property

from rdmo.questions.models import Catalog, Page, Question, QuestionSet, Section


class AnswerTree:

    def __init__(self, project, snapshot=None):
        self.project = project
        self.snapshot = snapshot

        # buffer for the resolved conditions: self.resolved_conditions[element][parent_set]
        self.resolved_conditions = defaultdict(lambda: defaultdict(dict))

    @cached_property
    def conditions(self):
        return {
            condition.id: condition for condition in self.project.catalog.conditions
        }

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
        # Main function of this class, which Computes the answer tree recursively.
        # First, it computes the catalog, section, and page nodes.
        # Then, it alternates between (value)set and questionset nodes until it reaches
        # the question nodes, which include the corresponding values as well as how much
        # this question counts to the count and total values for the progress.
        return self.compute_element_node(self.project.catalog)

    def compute_element_node(self, element, parent_set=None):
        # recursive function, which will be called for each element
        element_node = {
            'id': element.id,
            'uri': element.uri,
            'model': str(element._meta)
        }

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
            element_sets = self.compute_element_sets(element, parent_set)

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

        if isinstance(element, (Page, QuestionSet, Question)) and element.has_conditions:
            # for pages, questionsets and questions evaluate conditions
            element_node['hide'] = not self.resolve_conditions(element, parent_set)

            # if the element is hidden, do not it or its descendants
            if element_node['hide']:
                element_node['count'] = 0
                element_node['total'] = 0

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

        # aggregate count and total from the element nodes
        set_node['count'] = sum(element_node['count'] for element_node in set_node['elements'])
        set_node['total'] = sum(element_node['total'] for element_node in set_node['elements'])

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
                descendant_sets = self.filter_descendant_sets(descendant, parent_set)

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

        return sorted(element_sets)

    def compute_element_values(self, element, parent_set):
        set_prefix, set_index = parent_set

        # filter the values for this element and set
        element_values = list(filter(lambda v: all((
            v.attribute == element.attribute,
            v.set_prefix == set_prefix,
            v.set_index == set_index,
        )), self.values))

        if element_values:
            # if there are values, return them
            return [
                {
                    'id': value.id,
                    'is_empty': value.is_empty,
                    'collection_index': value.collection_index
                }
                for value in element_values
            ]
        else:
            # if no value is present, create one empty empty value
            return [
                {
                    'is_empty': True,
                    'collection_index': 0
                }
            ]

    def resolve_conditions(self, element, parent_set):
        # cache each resolved condition in self.resolved_conditions
        if self.resolved_conditions.get(element, {}).get(parent_set) is None:
            if parent_set:
                set_prefix, set_index = parent_set
                self.resolved_conditions[element][parent_set] = any(
                    self.conditions[condition.id].resolve(self.values, set_prefix, set_index)
                    for condition in element.conditions.all()
                )
            else:
                self.resolved_conditions[element][parent_set] = any(
                    self.conditions[condition.id].resolve(self.values)
                    for condition in element.conditions.all()
                )

        return self.resolved_conditions[element][parent_set]

    def filter_descendant_sets(self, descendant, parent_set):
        # find descendant sets and only include sets which are below the provided parent set
        descendant_sets = self.sets[descendant.attribute.id]

        if parent_set:
            parent_set_prefix, parent_set_index = parent_set
            if parent_set_prefix:
                descendant_set_prefix = f'{parent_set_prefix}|{parent_set_index}'
            else:
                descendant_set_prefix = str(parent_set_index)

            return set(filter(
                lambda s: (s[0] == descendant_set_prefix) or s[0].startswith(f'{descendant_set_prefix}|'),
                descendant_sets
            ))
        else:
            return descendant_sets
