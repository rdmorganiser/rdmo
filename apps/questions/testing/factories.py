import factory

from factory.django import DjangoModelFactory

from ..models import *


class CatalogFactory(DjangoModelFactory):

    class Meta:
        model = Catalog

    title_en = 'catalog en'
    title_de = 'catalog de'
    order = 1


class SectionFactory(DjangoModelFactory):

    class Meta:
        model = Section

    catalog = factory.SubFactory(CatalogFactory)
    order = 1

    title_en = 'section en'
    title_de = 'section de'


class SubsectionFactory(DjangoModelFactory):

    class Meta:
        model = Subsection

    section = factory.SubFactory(SectionFactory)
    order = 1

    title_en = 'subsection en'
    title_de = 'subsection de'


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
    widget_type = 'text'

    text_en = 'question text en'
    text_de = 'question text de'
