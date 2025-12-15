from collections import defaultdict

from rdmo.core.utils import markdown2html

from .models.value import Value


class AnswerTree:

    def __init__(self, catalog, values, verbose=None):
        self.catalog = catalog
        self.values = values
        self.verbose = tuple(verbose or ())

        self.sets = values.compute_sets()
        self.conditions = catalog.conditions.in_bulk()

        # buffer for the resolved conditions: self.resolved_conditions[element][parent_set]
        self.resolved_conditions = defaultdict(lambda: defaultdict(dict))

    def compute(self):
        # Main function of this class, which Computes the answer tree recursively.
        # First, it computes the catalog, section, and page nodes.
        # Then, it alternates between (value)set and questionset nodes until it reaches
        # the question nodes, which include the corresponding values as well as how much
        # this question counts to the count and total values for the progress.
        return self.compute_element_node(self.catalog)

    def compute_element_node(self, element, parent_set=None):
        # recursive function, which will be called for each element
        element_type = element._meta.model_name

        element_node = {
            'id': element.id,
            'model': element._meta.label_lower,
            'show': True,  # init show flag
        }

        if element_type in self.verbose:
            # optionally, add the rendered title, help and texts
            element_node.update({
                'uri': element.uri
            })

            if element_type in ['catalog', 'page', 'questionset']:
                element_node.update({
                    'title': markdown2html(element.title),
                    'help': markdown2html(element.help)
                })
            elif element_type == 'section':
                element_node.update({
                    'title': markdown2html(element.title)
                })
            elif element_type == 'question':
                element_node.update({
                    'text': markdown2html(element.text),
                    'help': markdown2html(element.help)
                })

        if element_type in ('page', 'questionset', 'question'):
            # for pages, questionsets and questions evaluate conditions
            if element.has_conditions:
                result = self.resolve_conditions(element, parent_set)

                # if the element is not shown, break the recursion
                if not result:
                    element_node['show'] = False
                    element_node['count'] = 0
                    element_node['total'] = 0

                    return element_node

        if element_type in ('catalog', 'section'):
            # for catalogs and sections we recurse to the next level of elements (sections, pages)
            element_node['elements'] = [
                self.compute_element_node(child_element)
                for child_element in element.elements
            ]

            # find the first element
            if element_type in self.verbose:
                element_node['first'] = element_node['elements'][0]['id']

            # aggregate count and total from the child elements
            element_node['count'] = sum(child_node['count'] for child_node in element_node['elements'])
            element_node['total'] = sum(child_node['total'] for child_node in element_node['elements'])

        elif element_type in ('page', 'questionset'):
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

        elif element_type == 'question':
            # for questions we add the text and the values and compute if this question
            # can be considered empty, meaning it has no or only empty values
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
        level = self.compute_set_level(parent_set)

        # for pages, add the sets for the attribute of the page
        if parent_set is None and element.attribute:
            element_sets.update(
                (set_prefix, set_index)
                for set_prefix, set_index in self.sets[element.attribute.id]
                if set_prefix == ''  # only include sets for pages
            )

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
                        element_set = self.compute_ancestor_set(descendant_set_prefix, level)
                        if element_set is not None:
                            element_sets.add(element_set)

        # create one empty set for non-collection pages/questionsets
        if not element.is_collection:
            set_prefix = self.compute_child_set_prefix(parent_set)
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
                self.compute_value_node(value)
                for value in element_values
            ]
        else:
            # if no value is present, create one empty value
            return [
                self.compute_value_node(Value())
            ]

    def compute_value_node(self, value=None):
        if 'value' in self.verbose:
            return value.as_dict
        else:
            return {
                'collection_index': value.collection_index,
                'is_empty': value.is_empty
            }

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
            child_set_prefix = self.compute_child_set_prefix(parent_set)

            return {
                (set_prefix, set_index)
                for set_prefix, set_index in descendant_sets
                if set_prefix == child_set_prefix or set_prefix.startswith(f'{child_set_prefix}|')
            }
        else:
            return descendant_sets

    @staticmethod
    def compute_set_level(parent_set):
        # compute the level in the page/questionsets hierarchy from a parent set
        # if no parent set is provided the level is 0
        if parent_set:
            set_prefix, _ = parent_set
            return set_prefix.count('|') + 1
        else:
            return 0

    @staticmethod
    def compute_child_set_prefix(parent_set):
        # compute the set_prefix for child sets from a parent set
        if parent_set:
            set_prefix, set_index = parent_set
            if set_prefix:
                return f'{set_prefix}|{set_index}'
            else:
                return str(set_index)
        else:
            return ''

    @staticmethod
    def compute_ancestor_set(descendant_set_prefix, level):
        # compute the ancestor set of a given level for a descendant set
        # exclude sets with an empty set_prefix, this can happen in wrongly configured
        # catalogs, when a page and one of the descendant have the same attribute
        if descendant_set_prefix:
            parts = descendant_set_prefix.split('|')
            if level < len(parts):
                return ('|'.join(parts[:level]) if level else '', int(parts[level]))
