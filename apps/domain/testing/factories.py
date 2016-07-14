import factory

from factory.django import DjangoModelFactory

from ..models import *


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


class RangeFactory(DjangoModelFactory):

    class Meta:
        model = Range
        django_get_or_create = ('id', )

    attribute = factory.SubFactory('apps.domain.testing.factories.AttributeFactory')

    id = factory.Sequence(lambda n: n)
    minimum = 0.0
    maximum = 100.0
    step = 10


class AttributeEntityFactory(DjangoModelFactory):

    class Meta:
        model = AttributeEntity
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    title = 'title'
    is_collection = False


class AttributeFactory(DjangoModelFactory):

    class Meta:
        model = Attribute
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    title = 'title'
    is_collection = False

    value_type = 'text'

    @factory.post_generation
    def post_generation(self, create, extracted, **kwargs):
        if self.value_type == 'options':
            OptionFactory(id=10000 + self.id, attribute=self, order=1, text_en='A', text_de='A')
            OptionFactory(id=20000 + self.id, attribute=self, order=2, text_en='B', text_de='B')
            OptionFactory(id=30000 + self.id, attribute=self, order=3, text_en='C', text_de='C')
            OptionFactory(id=40000 + self.id, attribute=self, order=4, text_en='Other', text_de='Sonstige', additional_input=True)

        elif self.value_type == 'range':
            RangeFactory(id=20000 + self.id, attribute=self)


class VerboseNameFactory(DjangoModelFactory):

    class Meta:
        model = VerboseName
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    attribute_entity = factory.SubFactory(AttributeEntityFactory)

    name_en = 'name_en'
    name_de = 'name_de'

    name_plural_en = 'name_plural_en'
    name_plural_de = 'name_plural_de'


class ConditionFactory(DjangoModelFactory):

    class Meta:
        model = Condition
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    attribute_entity = factory.SubFactory(AttributeEntityFactory)

    source_attribute = factory.SubFactory(AttributeFactory)
    relation = 'eq'
