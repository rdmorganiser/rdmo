import factory

from factory.django import DjangoModelFactory

from ..models import *


class OptionSetFactory(DjangoModelFactory):

    class Meta:
        model = OptionSet
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    title = 'title'
    order = 1

    @factory.post_generation
    def post_generation(self, create, extracted, **kwargs):
        OptionFactory(id=10000 + self.id, optionset=self, title='a', order=1, text_en='A', text_de='A')
        OptionFactory(id=20000 + self.id, optionset=self, title='b', order=2, text_en='B', text_de='B')
        OptionFactory(id=30000 + self.id, optionset=self, title='c', order=3, text_en='C', text_de='C')
        OptionFactory(id=40000 + self.id, optionset=self, title='other', order=4, text_en='Other', text_de='Sonstige', additional_input=True)


class OptionFactory(DjangoModelFactory):

    class Meta:
        model = Option
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    title = 'title'
    order = 1

    text_en = 'text_en'
    text_de = 'text_de'

    additional_input = False
