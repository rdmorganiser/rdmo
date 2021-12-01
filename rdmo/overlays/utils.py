from django.conf import settings


def get_overlays(url_name):
    overlays = settings.OVERLAYS.get(url_name)[:]

    if not settings.PROJECT_ISSUES and 'project-issues' in overlays:
        overlays.remove('project-issues')

    if not settings.PROJECT_VIEWS and 'project-views' in overlays:
        overlays.remove('project-views')

    if not settings.PROJECT_EXPORTS and 'export-project' in overlays:
        overlays.remove('export-project')

    if not settings.PROJECT_IMPORTS and 'import-project' in overlays:
        overlays.remove('import-project')

    return overlays
