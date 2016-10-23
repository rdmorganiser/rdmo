import factory

from factory.django import DjangoModelFactory

from ..models import *


class OptionSetFactory(DjangoModelFactory):

    class Meta:
        model = OptionSet
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    attribute = factory.SubFactory('apps.domain.testing.factories.AttributeFactory')
    order = 1


class OptionFactory(DjangoModelFactory):

    class Meta:
        model = Option
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    attribute = factory.SubFactory('apps.domain.testing.factories.AttributeFactory')
    order = 1

    text_en = 'text_en'
    text_de = 'text_de'

    additional_input = False
