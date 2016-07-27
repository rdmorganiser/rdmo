import datetime
import factory

from factory.django import DjangoModelFactory

from ..models import *


class TaskFactory(DjangoModelFactory):

    class Meta:
        model = Task
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)
    attribute = factory.SubFactory('apps.domain.testing.factories.AttributeFactory')

    time_period = datetime.timedelta(60)

    title_en = 'title_en'
    title_de = 'title_de'

    text_en = 'text_en'
    text_de = 'text_de'
