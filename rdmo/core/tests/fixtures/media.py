import shutil
from pathlib import Path

import pytest


@pytest.fixture
def files(settings, tmp_path):
    """Create a temporary MEDIA_ROOT directory and copy test data into it."""
    media_path = Path(settings.BASE_DIR) / 'media'
    settings.MEDIA_ROOT = tmp_path.joinpath("media")
    shutil.copytree(media_path, settings.MEDIA_ROOT)
    return settings.MEDIA_ROOT
