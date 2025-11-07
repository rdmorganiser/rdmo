from rdmo.core.import_helpers import ElementImportHelper, ExtraFieldHelper

from .models import Plugin
from .validators import PluginLockedValidator, PluginUniqueURIValidator

import_helper_plugin = ElementImportHelper(
    model=Plugin,
    validators=(PluginLockedValidator, PluginUniqueURIValidator),
    lang_fields=('title', 'help'),
    extra_fields=(
        ExtraFieldHelper(field_name='python_path'),
        ExtraFieldHelper(field_name='plugin_settings', overwrite_in_element=True),
        ExtraFieldHelper(field_name='available', overwrite_in_element=True),
        ExtraFieldHelper(field_name='locked'),
        ExtraFieldHelper(field_name='order'),
    ),
    add_current_site_sites = True,
)
