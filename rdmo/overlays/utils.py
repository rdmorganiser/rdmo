from django.conf import settings


def get_overlays(url_name):
    overlays = settings.OVERLAYS.get(url_name)[:]

    if not settings.PROJECT_ISSUES:
        overlays.remove('project-issues')

    if not settings.PROJECT_VIEWS:
        overlays.remove('project-views')

    if not settings.PROJECT_EXPORTS:
        overlays.remove('export-project')

    if not settings.PROJECT_IMPORTS:
        overlays.remove('import-project')

    return overlays
