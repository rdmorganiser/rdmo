import json
from pathlib import Path

import pytest

from django.conf import settings


@pytest.fixture
def json_data():
    json_file = Path(settings.BASE_DIR) / 'import' / 'catalogs.json'
    return {'elements': json.loads(json_file.read_text())}
