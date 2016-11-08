import factory

from factory.django import DjangoModelFactory

from ..models import *


class CatalogFactory(DjangoModelFactory):

    class Meta:
        model = Catalog

    title_en = factory.SelfAttribute('title', default='catalog')
    title_de = factory.SelfAttribute('title', default='catalog')
    order = 1


class SectionFactory(DjangoModelFactory):

    class Meta:
        model = Section

    catalog = factory.SubFactory(CatalogFactory)
    order = 1

    title_en = factory.SelfAttribute('title', default='section')
    title_de = factory.SelfAttribute('title', default='section')


class SubsectionFactory(DjangoModelFactory):

    class Meta:
        model = Subsection

    section = factory.SubFactory(SectionFactory)
    order = 1

    title_en = factory.SelfAttribute('title', default='subsection')
    title_de = factory.SelfAttribute('title', default='subsection')


class QuestionEntityFactory(DjangoModelFactory):

    class Meta:
        model = QuestionEntity

    subsection = factory.SubFactory(SubsectionFactory)
    order = 1

    help_en = 'question entity help en'
    help_de = 'question entity help de'


class QuestionFactory(DjangoModelFactory):

    class Meta:
        model = Question

    subsection = factory.SubFactory(SubsectionFactory)
    order = 1

    help_en = 'question help en'
    help_de = 'question help de'

    text_en = factory.SelfAttribute('text', default='question')
    text_de = factory.SelfAttribute('text', default='question')

    widget_type = 'text'
