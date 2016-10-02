import factory

from apps.questions.testing.factories import CatalogFactory

from ..models import *


class SnapshotFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Snapshot

    project = factory.SubFactory('apps.projects.factories.ProjectFactory')


class ProjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Project

    title = 'Test'
    description = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est. Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est. Lorem ipsum dolor sit amet.'
    catalog = factory.SubFactory(CatalogFactory)

    @factory.post_generation
    def owner(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.owner.add(item)
