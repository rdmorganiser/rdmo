from django.db import models


class PageQuestion(models.Model):

    page = models.ForeignKey(
        'Page', on_delete=models.CASCADE, related_name='page_questions'
    )
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='question_pages'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('page', 'order')

    def __str__(self):
        return f'{self.page} / {self.question} [{self.order}]'

    @property
    def element(self):
        return self.question
