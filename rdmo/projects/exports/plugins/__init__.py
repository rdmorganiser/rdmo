from rdmo.core.plugins import Plugin


class Export(Plugin):
    download = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = None
        self.snapshot = None
