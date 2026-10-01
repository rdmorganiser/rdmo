from django.utils.timezone import now

from rdmo.core.models import Model as TimestampedModel
from rdmo.options.models import Option

from ..models import Catalog, Page, Question, QuestionSet, Section

URI_PREFIX = 'https://example.com/terms'


def _primary_label(model, uri_path):
    if model in (Option, Question):
        return {'text_lang1': f'{model.__name__} {uri_path}'}
    if model in (Catalog, Section, Page, QuestionSet):
        return {'title_lang1': f'{model.__name__} {uri_path}'}
    return {}


def create_element(model, uri_path, **kwargs):
    fields = {**_primary_label(model, uri_path), **kwargs}
    if model is Question:
        fields.setdefault('widget_type', 'text')
        fields.setdefault('value_type', 'text')
    return model.objects.create(uri_prefix=URI_PREFIX, uri_path=uri_path, **fields)


def create_elements(model, count, uri_path, **kwargs):
    paths = [f'{uri_path}-{index:04d}' for index in range(count)]
    if model is Question:
        kwargs.setdefault('widget_type', 'text')
        kwargs.setdefault('value_type', 'text')
    if issubclass(model, TimestampedModel):
        # bulk_create bypasses save(), which normally sets these required timestamps.
        timestamp = now()
        kwargs.setdefault('created', timestamp)
        kwargs.setdefault('updated', timestamp)
    model.objects.bulk_create([
        model(uri=model.build_uri(URI_PREFIX, path), uri_prefix=URI_PREFIX, uri_path=path,
              **{**_primary_label(model, path), **kwargs})
        for path in paths
    ])
    # Re-fetch primary keys because bulk_create does not populate them on every database backend.
    elements = list(model.objects.filter(
        uri_prefix=URI_PREFIX, uri_path__startswith=f'{uri_path}-'
    ).order_by('uri_path'))
    assert len(elements) == count
    return elements
