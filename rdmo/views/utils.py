from collections import defaultdict
from urllib.parse import urlparse

from django.utils.functional import cached_property

from mptt.utils import get_cached_trees


class ProjectWrapper:

    def __init__(self, project, snapshot=None):
        self._project = project
        self._catalog = project.catalog
        self._snapshot = snapshot
        self._resolved_conditions = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def __str__(self):
        return str(self._project.title)

    @property
    def id(self):
        return self._project.id

    @property
    def title(self):
        return self._project.title

    @property
    def description(self):
        return self._project.description

    @property
    def created(self):
        return self._project.created

    @property
    def updated(self):
        return self._project.updated

    @property
    def snapshot(self):
        if self._snapshot:
            return {
                'id': self._snapshot.id,
                'title': self._snapshot.title,
                'description': self._snapshot.description,
                'created': self._snapshot.created,
                'updated': self._snapshot.updated
            }
        else:
            return {}

    @cached_property
    def descendants(self):
        return [ProjectWrapper(descendant) for descendant in self._project.get_descendants()]

    @cached_property
    def children(self):
        return [ProjectWrapper(child) for child in self._project.get_children()]

    @cached_property
    def tree(self):
        cached_trees = get_cached_trees(self._project.get_descendants())
        return self._build_tree(cached_trees)

    @cached_property
    def conditions(self):
        conditions = {}
        for condition in self._conditions:
            conditions[condition.uri] = conditions[condition.uri_path] = self._resolve_condition(condition)
        return conditions

    @cached_property
    def catalog(self):
        return self._catalog.to_dict()

    @cached_property
    def questions(self):
        def walk(elements):
            questions = []
            for element in elements:
                if element.get('elements'):
                    questions += walk(element.get('elements'))
                else:
                    questions.append(element)
            return questions

        return walk(self.catalog['elements'])

    @cached_property
    def _values(self):
        return list(self._project.values.filter(snapshot=self._snapshot).select_related('attribute', 'option'))

    @cached_property
    def _conditions(self):
        from rdmo.conditions.models import Condition
        return list(Condition.objects.select_related('source', 'target_option'))

    def _get_values(self, attribute, set_prefix='*', set_index='*', index='*'):
        values = self._values

        if urlparse(attribute).scheme:
            values = filter(lambda value: value.attribute and (value.attribute.uri == attribute), values)
        else:
            values = filter(lambda value: value.attribute and (value.attribute.path == attribute), values)

        if set_prefix != '*':
            values = filter(lambda value: value.set_prefix == set_prefix, values)

        if set_index != '*':
            values = filter(lambda value: value.set_index == set_index, values)

        if index != '*':
            values = filter(lambda value: value.collection_index == index, values)

        return [value.as_dict for value in values]

    def _check_element(self, element, set_prefix=None, set_index=None):
        conditions = set(filter(lambda condition: condition.uri in element['conditions'], self._conditions))
        for ancestor in element.get('ancestors', []):
            conditions.update(filter(lambda condition: condition.uri in ancestor['conditions'], self._conditions))

        return self._resolve_conditions(conditions, set_prefix=set_prefix, set_index=set_index)

    def _check_condition(self, condition, set_prefix=None, set_index=None):
        conditions = self._conditions

        if urlparse(condition).scheme:
            conditions = filter(lambda c: c.uri == condition, conditions)
        else:
            conditions = filter(lambda c: c.uri_path == condition, conditions)

        return self._resolve_conditions(conditions, set_prefix=set_prefix, set_index=set_index)

    def _resolve_conditions(self, conditions, set_prefix=None, set_index=None):
        # caches the result of the check in the wrapper
        if conditions:
            for condition in conditions:
                if self._resolve_condition(condition, set_prefix, set_index):
                    return True
            return False
        else:
            return True

    def _resolve_condition(self, condition, set_prefix=None, set_index=None):
        # caches the result of the check in the wrapper
        if self._resolved_conditions[condition.id][set_prefix][set_index] == []:
            self._resolved_conditions[condition.id][set_prefix][set_index] = \
                condition.resolve(self._values, set_prefix, set_index)

        return self._resolved_conditions[condition.id][set_prefix][set_index]

    def _build_tree(self, projects):
        return [{
            'id': project.id,
            'level': project.level,
            'children': self.build_tree(project.get_children())
        } for project in projects]
