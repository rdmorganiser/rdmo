from django.db import models


class CatalogSection(models.Model):

    catalog = models.ForeignKey(
        'Catalog', on_delete=models.CASCADE, related_name='catalog_sections'
    )
    section = models.ForeignKey(
        'Section', on_delete=models.CASCADE, related_name='section_catalogs'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('catalog', 'order')

    def __str__(self):
        return f'{self.catalog} / {self.section} [{self.order}]'
