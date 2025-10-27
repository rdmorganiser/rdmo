from rdmo.options.providers import Provider


class TestOptionSetProvider(Provider):
    search = False
    refresh = False

    def get_options(self, project, search=None, user=None, site=None):
        return [
            {"external_id": "opt1", "text": "Option One"},
            {"external_id": "opt2", "text": "Option Two"},
            {"external_id": "opt3", "text": "Option Three"},
        ]
