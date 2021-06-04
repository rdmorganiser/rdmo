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


class QuestionSetQuerySet(models.QuerySet):

    def order_by_catalog(self, catalog):
        return self.filter(section__catalog=catalog, questionset=None).order_by('section__order', 'order')

    def _get_pk_list(self, pk):
        catalog = self.get(pk=pk).section.catalog

        pk_list = list(self.order_by_catalog(catalog).values_list('pk', flat=True))
        current_index = pk_list.index(int(pk))

        return pk_list, current_index

    def get_prev(self, pk):
        pk_list, current_index = self._get_pk_list(pk)

        if current_index > 0:
            prev_pk = pk_list[current_index - 1]
            return self.get(pk=prev_pk)
        else:
            raise self.model.DoesNotExist('QuestionSet has no previous QuestionSet. It is the first one.')

    def get_next(self, pk):
        pk_list, current_index = self._get_pk_list(pk)

        if current_index < len(pk_list) - 1:
            next_pk = pk_list[current_index + 1]
            return self.get(pk=next_pk)
        else:
            raise self.model.DoesNotExist('QuestionSet has no next QuestionSet. It is the last one.')


class QuestionSetManager(models.Manager):

    def get_queryset(self):
        return QuestionSetQuerySet(self.model, using=self._db)

    def order_by_catalog(self, catalog):
        return self.get_queryset().order_by_catalog(catalog)

    def get_prev(self, pk):
        return self.get_queryset().get_prev(pk)

    def get_next(self, pk):
        return self.get_queryset().get_next(pk)


class QuestionQuerySet(models.QuerySet):

    def order_by_catalog(self, catalog):
        return self.filter(questionset__section__catalog=catalog).order_by('questionset__section__order', 'questionset__order', 'order')

    def filter_by_catalog(self, catalog):
        return self.filter(questionset__section__catalog=catalog)


class QuestionManager(models.Manager):

    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def order_by_catalog(self, catalog):
        return self.get_queryset().order_by_catalog(catalog)

    def filter_by_catalog(self, catalog):
        return self.get_queryset().filter_by_catalog(catalog)
