from rdmo.core.plugins import Plugin


class Export(Plugin):
    download = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = None
        self.snapshot = None

    def get_set(self, path, set_prefix=''):
        return self.project.values.filter(snapshot=self.snapshot, attribute__path=path, set_prefix=set_prefix) \
                                  .order_by('set_index', 'collection_index')

    def get_values(self, path, set_prefix='', set_index=0):
        return self.project.values.filter(snapshot=self.snapshot, attribute__path=path,
                                          set_prefix=set_prefix, set_index=set_index) \
                                  .order_by('collection_index')

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

    def get_timestamp(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index].value.isoformat()
        except (IndexError, AttributeError):
            return None

    def get_year(self, path, set_prefix='', set_index=0, collection_index=0):
        try:
            return self.get_values(path, set_prefix=set_prefix, set_index=set_index)[collection_index].value.year
        except (IndexError, AttributeError):
            return None

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
