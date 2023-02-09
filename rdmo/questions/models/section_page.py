from django.db import models


class SectionPage(models.Model):

    section = models.ForeignKey(
        'Section', on_delete=models.CASCADE, related_name='section_pages'
    )
    page = models.ForeignKey(
        'Page', on_delete=models.CASCADE, related_name='page_sections'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('section', 'order')

    def __str__(self):
        return f'{self.section} / {self.page} [{self.order}]'
