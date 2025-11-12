from django.conf import settings

RDMORGANISER_URI_PREFIX = "https://rdmorganiser.github.io/terms"

def get_default_uri_prefix_for_python_path(python_path: str) -> str:
    if python_path.startswith('rdmo.'):
        return RDMORGANISER_URI_PREFIX
    else:
        return settings.DEFAULT_URI_PREFIX
