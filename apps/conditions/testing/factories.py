import factory

from factory.django import DjangoModelFactory

from ..models import *


class ConditionFactory(DjangoModelFactory):

    class Meta:
        model = Condition
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)

    title = 'condition'

    source = factory.SubFactory('apps.domain.testing.factories.AttributeFactory')
    relation = 'eq'
    target_text = '1'
    target_option = None
