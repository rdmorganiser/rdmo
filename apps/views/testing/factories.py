import factory

from factory.django import DjangoModelFactory

from ..models import *


class ViewFactory(DjangoModelFactory):

    class Meta:
        model = View
        django_get_or_create = ('id', )

    id = factory.Sequence(lambda n: n)

    title = 'title'
    description = 'description'
    template = '<h1>View</h1>'
