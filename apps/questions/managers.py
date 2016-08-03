from django.db import models


class QuestionEntityQuerySet(models.QuerySet):
    def order_by_catalog(self, catalog):
        return self.filter(subsection__section__catalog=catalog) \
                   .filter(question__parent=None) \
                   .order_by('subsection__section__order', 'subsection__order', 'order')

    def _get_pk_list(self, pk):
        catalog = self.get(pk=pk).subsection.section.catalog

        pk_list = list(self.order_by_catalog(catalog).values_list('pk', flat=True))
        current_index = pk_list.index(int(pk))

        return pk_list, current_index

    def get_prev(self, pk):
        pk_list, current_index = self._get_pk_list(pk)

        if current_index > 0:
            prev_pk = pk_list[current_index - 1]
            return self.get(pk=prev_pk)
        else:
            raise self.model.DoesNotExist('QuestionEntity has no previous QuestionEntity. It is the first one.')

    def get_next(self, pk):
        pk_list, current_index = self._get_pk_list(pk)

        if current_index < len(pk_list) - 1:
            next_pk = pk_list[current_index + 1]
            return self.get(pk=next_pk)
        else:
            raise self.model.DoesNotExist('QuestionEntity has no next QuestionEntity. It is the last one.')

    def get_progress(self, pk):
        pk_list, current_index = self._get_pk_list(pk)

        return (100.0 * (1 + current_index)/len(pk_list))


class QuestionEntityManager(models.Manager):

    def get_queryset(self):
        return QuestionEntityQuerySet(self.model, using=self._db)

    def order_by_catalog(self, catalog):
        return self.get_queryset().order_by_catalog(catalog)

    def get_prev(self, pk):
        return self.get_queryset().get_prev(pk)

    def get_next(self, pk):
        return self.get_queryset().get_next(pk)

    def get_progress(self, pk):
        return self.get_queryset().get_progress(pk)
