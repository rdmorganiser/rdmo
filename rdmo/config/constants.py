from django.db.models import TextChoices


class PLUGIN_TYPES(TextChoices):
    PROJECT_EXPORT = "project_export", "Project export"
    PROJECT_SNAPSHOT_EXPORT = "project_snapshot_export", "Project snapshot export"
    PROJECT_IMPORT = "project_import", "Project import"
    PROJECT_ISSUE_PROVIDER = "project_issue_provider", "Project issue provider"
    OPTIONSET_PROVIDER = "optionset_provider", "Optionset provider"
