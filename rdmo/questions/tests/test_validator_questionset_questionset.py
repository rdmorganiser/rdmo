from contextlib import nullcontext

import pytest

from django.core.exceptions import ValidationError

from rest_framework.exceptions import ValidationError as RestFrameworkValidationError

from ..models import QuestionSet
from ..serializers.v1 import QuestionSetSerializer
from ..validators import QuestionSetQuestionSetValidator


@pytest.mark.parametrize('questionset_uri,success', [
    ('http://example.com/terms/questions/catalog/blocks/single/block', True),
    ('http://example.com/terms/questions/catalog/blocks/set/block/block', False),
    ('http://example.com/terms/questions/catalog/blocks/set/block', False),
])
def test_update(db, questionset_uri, success):
    instance = QuestionSet.objects.get(uri='http://example.com/terms/questions/catalog/blocks/set/block/block')

    with nullcontext() if success else pytest.raises(ValidationError):
        QuestionSetQuestionSetValidator(instance)({
            'questionsets': [
                QuestionSet.objects.get(uri=questionset_uri)
            ]
        })


@pytest.mark.parametrize('questionset_uri,success', [
    ('http://example.com/terms/questions/catalog/blocks/single/block', True),
    ('http://example.com/terms/questions/catalog/blocks/set/block/block', False),
    ('http://example.com/terms/questions/catalog/blocks/set/block', False),
])
def test_serializer_update(db, questionset_uri, success):
    instance = QuestionSet.objects.get(uri='http://example.com/terms/questions/catalog/blocks/set/block/block')

    validator = QuestionSetQuestionSetValidator()
    serializer = QuestionSetSerializer(instance=instance)

    with nullcontext() if success else pytest.raises(RestFrameworkValidationError):
        validator({
            'questionsets': [
                QuestionSet.objects.get(uri=questionset_uri)
            ]
        }, serializer)
