from django.db import models


class QuestionSetQuestionSet(models.Model):

    parent = models.ForeignKey(
        'QuestionSet', on_delete=models.CASCADE, related_name='questionset_questionsets'
    )
    questionset = models.ForeignKey(
        'QuestionSet', on_delete=models.CASCADE, related_name='questionset_parents'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('parent', 'order')

    def __str__(self):
        return f'{self.parent} / {self.questionset} [{self.order}]'

    @property
    def element(self):
        return self.questionset
