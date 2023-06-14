from django.db import models


class PageQuestionSet(models.Model):

    page = models.ForeignKey(
        'Page', on_delete=models.CASCADE, related_name='page_questionsets'
    )
    questionset = models.ForeignKey(
        'QuestionSet', on_delete=models.CASCADE, related_name='questionset_pages'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('page', 'order')

    def __str__(self):
        return f'{self.page} / {self.questionset} [{self.order}]'

    @property
    def element(self):
        return self.questionset
