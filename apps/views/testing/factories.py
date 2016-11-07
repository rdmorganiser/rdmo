import factory

from factory.django import DjangoModelFactory

from ..models import *


class ViewFactory(DjangoModelFactory):

    class Meta:
        model = View

    title = 'title'
    description = 'description'
    template = '<h1>View</h1>'
