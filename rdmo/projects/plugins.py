from urllib.parse import urlparse

from django.utils.functional import cached_property

import iso8601


class ProjectValues:
    '''
    Read access to the values of a project (or one of its snapshots) for plugins. All values
    are fetched with one query on first access and filtered in Python afterwards, therefore
    the instance should be cached in the plugin:

        class ExampleExport(Export):

            @cached_property
            def values(self):
                return ProjectValues(self.project, self.snapshot)
    '''

    def __init__(self, project, snapshot=None):
        self.project = project
        self.snapshot = snapshot

    @cached_property
    def _values(self):
        return list(self.project.values.filter(snapshot=self.snapshot).select_related('attribute', 'option'))

    def filter_values(self, attribute, set_prefix='*', set_index='*', collection_index='*'):
        # filter the values in Python, the attribute can be given as uri or path, '*' matches everything
        values = self._values

        if urlparse(attribute).scheme:
            values = filter(lambda value: value.attribute and (value.attribute.uri == attribute), values)
        else:
            values = filter(lambda value: value.attribute and (value.attribute.path == attribute), values)

        if set_prefix != '*':
            values = filter(lambda value: value.set_prefix == set_prefix, values)

        if set_index != '*':
            values = filter(lambda value: value.set_index == set_index, values)

        if collection_index != '*':
            values = filter(lambda value: value.collection_index == collection_index, values)

        return sorted(values, key=lambda value: (value.set_index, value.collection_index))

    def get_set(self, path, set_prefix=''):
        return self.filter_values(path, set_prefix=set_prefix)

    def get_values(self, path, set_prefix='', set_index=0):
        return self.filter_values(path, set_prefix=set_prefix, set_index=set_index)

    def get_value(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index]
        except IndexError:
            return None

    def get_text(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index].text
        except IndexError:
            return None

    def get_date(self, path, set_prefix='', set_index=0, collection_index=0):
        # parse the text of the value directly, since value.value depends on the value_type
        value = self.get_value(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        if value and value.text:
            try:
                return iso8601.parse_date(value.text).date()
            except iso8601.ParseError:
                pass
        return None

    def get_timestamp(self, path, set_prefix='', set_index=0, collection_index=0):
        date = self.get_date(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        return date.isoformat() if date else None

    def get_year(self, path, set_prefix='', set_index=0, collection_index=0):
        date = self.get_date(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        return date.year if date else None

    def get_list(self, path, set_prefix='', set_index=0):
        values = self.get_values(path, set_prefix=set_prefix, set_index=set_index)
        return [value.text for value in values if value.text]

    def get_bool(self, path, set_prefix='', set_index=0, collection_index=0):
        value = self.get_value(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        if value:
            return True if value.text == '1' else False
        else:
            return None

    def get_option(self, options, path, set_prefix='', set_index=0, collection_index=0, default=None):
        value = self.get_value(path, set_prefix=set_prefix, set_index=set_index, collection_index=collection_index)
        if value and value.option:
            # lookup option dict in class
            return options.get(value.option.uri_path, default)
        else:
            return default
