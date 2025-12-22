from enum import Enum


class PluginType(str, Enum):
    PROJECT_EXPORT = "project_export"
    PROJECT_SNAPSHOT_EXPORT = "project_snapshot_export"
    PROJECT_IMPORT = "project_import"
    PROJECT_ISSUE_PROVIDER = "project_issue_provider"
    OPTIONSET_PROVIDER = "optionset_provider"
