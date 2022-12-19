from django.db import models

from rdmo.core.managers import (AvailabilityManagerMixin,
                                AvailabilityQuerySetMixin,
                                CurrentSiteManagerMixin,
                                CurrentSiteQuerySetMixin, GroupsManagerMixin,
                                GroupsQuerySetMixin)


class CatalogQuestionSet(CurrentSiteQuerySetMixin, GroupsQuerySetMixin, AvailabilityQuerySetMixin, models.QuerySet):

    def filter_catalog(self, catalog):
        return self.filter(models.Q(catalogs=None) | models.Q(catalogs=catalog))


class CatalogManager(CurrentSiteManagerMixin, GroupsManagerMixin, AvailabilityManagerMixin, models.Manager):

    def get_queryset(self):
        return CatalogQuestionSet(self.model, using=self._db)

    def filter_catalog(self, catalog):
        return self.get_queryset().filter_catalog(catalog)


class QuestionQuerySet(models.QuerySet):

    def filter_by_catalog(self, catalog):
        models.prefetch_related_objects([catalog],
                                        'sections__pages__questionsets__questionsets__questions',
                                        'sections__pages__questionsets__questions',
                                        'sections__pages__questions')
        descendants = catalog.get_descendants()
        question_ids = set([descendant.id for descendant in descendants if isinstance(descendant, self.model)])
        return self.filter(id__in=question_ids)


class QuestionManager(models.Manager):

    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def filter_by_catalog(self, catalog):
        return self.get_queryset().filter_by_catalog(catalog)
