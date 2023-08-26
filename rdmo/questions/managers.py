from django.db import models

from rdmo.core.managers import (
    AvailabilityManagerMixin,
    AvailabilityQuerySetMixin,
    CurrentSiteManagerMixin,
    CurrentSiteQuerySetMixin,
    GroupsManagerMixin,
    GroupsQuerySetMixin,
)


class CatalogQuestionSet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin, models.QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))

    def prefetch_elements(self):
        return self.prefetch_related(*self.model.prefetch_lookups)


class CatalogManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self):
        return CatalogQuestionSet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)

    def prefetch_elements(self):
        return self.get_queryset().prefetch_elements()


class SectionQuerySet(models.QuerySet):

    def prefetch_elements(self):
        return self.prefetch_related(*self.model.prefetch_lookups)


class SectionManager(models.Manager):

    def get_queryset(self):
        return SectionQuerySet(self.model, using=self._db)

    def prefetch_elements(self):
        return self.get_queryset().prefetch_elements()


class PageQuerySet(models.QuerySet):

    def prefetch_elements(self):
        return self.prefetch_related(*self.model.prefetch_lookups)

    def filter_by_catalog(self, catalog):
        ids = [descendant.id for descendant in catalog.descendants if isinstance(descendant, self.model)]
        return self.filter(id__in=ids)


class PageManager(models.Manager):

    def get_queryset(self):
        return PageQuerySet(self.model, using=self._db)

    def filter_by_catalog(self, catalog):
        return self.get_queryset().filter_by_catalog(catalog)

    def prefetch_elements(self):
        return self.get_queryset().prefetch_elements()


class QuestionSetQuerySet(models.QuerySet):

    def prefetch_elements(self):
        return self.prefetch_related(*self.model.prefetch_lookups)

    def filter_by_catalog(self, catalog):
        ids = [descendant.id for descendant in catalog.descendants if isinstance(descendant, self.model)]
        return self.filter(id__in=ids)


class QuestionSetManager(models.Manager):

    def get_queryset(self):
        return QuestionSetQuerySet(self.model, using=self._db)

    def filter_by_catalog(self, catalog):
        return self.get_queryset().filter_by_catalog(catalog)


class QuestionQuerySet(models.QuerySet):

    def prefetch_elements(self):
        return self.prefetch_related(*self.model.prefetch_lookups)

    def filter_by_catalog(self, catalog):
        ids = [descendant.id for descendant in catalog.descendants if isinstance(descendant, self.model)]
        return self.filter(id__in=ids)


class QuestionManager(models.Manager):

    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def filter_by_catalog(self, catalog):
        return self.get_queryset().filter_by_catalog(catalog)

    def prefetch_elements(self):
        return self.get_queryset().prefetch_elements()
