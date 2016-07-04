import factory

from factory.django import DjangoModelFactory

from ..models import *


class AttributeEntityFactory(DjangoModelFactory):

    class Meta:
        model = AttributeEntity

    title = 'title'
    is_collection = False


class AttributeFactory(DjangoModelFactory):

    class Meta:
        model = Attribute

    title = 'title'
    is_collection = False


class OptionFactory(DjangoModelFactory):

    class Meta:
        model = Option

    attribute = factory.SubFactory(AttributeFactory)
    order = 1

    text_en = 'text_en'
    text_de = 'text_de'

    additional_input = False


class RangeFactory(DjangoModelFactory):

    class Meta:
        model = Range

    attribute = factory.SubFactory(AttributeFactory)

    minimum = 0.0
    maximum = 100.0
    step = 10


class VerboseNameFactory(DjangoModelFactory):

    class Meta:
        model = VerboseName

    attribute_entity = factory.SubFactory(AttributeEntityFactory)

    name_en = 'name_en'
    name_de = 'name_de'

    name_plural_en = 'name_plural_en'
    name_plural_de = 'name_plural_de'


class ConditionFactory(DjangoModelFactory):

    class Meta:
        model = Condition

    attribute_entity = factory.SubFactory(AttributeEntityFactory)

    source_attribute = factory.SubFactory(AttributeFactory)
    relation = 'eq'
