import pytest

from rdmo.domain.models import Attribute

from ..models import Value


@pytest.mark.parametrize('set_value_id', [85, 148])  # current values and snapshot 1
@pytest.mark.parametrize('set_prefix', ['10', '11'])
def test_filter_set_excludes_sibling_prefix(db, set_value_id, set_prefix):
    # Arrange: tab 2 has index 1; sibling answers use prefixes 10 or 11.
    set_value = Value.objects.get(id=set_value_id)
    attribute = Attribute.objects.get(uri='http://example.com/terms/domain/blocks/a')
    sibling_value = Value.objects.create(
        project=set_value.project, snapshot=set_value.snapshot, attribute=attribute,
        set_prefix=set_prefix, text='Sibling answer',
    )

    # Act: collect the selected tab's answers.
    values = Value.objects.all().filter_set(set_value)

    # Assert: a matching string prefix must not include a sibling's answer.
    assert not values.filter(id=sibling_value.id).exists()
