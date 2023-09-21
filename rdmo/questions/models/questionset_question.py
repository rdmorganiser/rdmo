from django.db import models


class QuestionSetQuestion(models.Model):

    questionset = models.ForeignKey(
        'QuestionSet', on_delete=models.CASCADE, related_name='questionset_questions'
    )
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='question_questionsets'
    )
    order = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ('questionset', 'order')

    def __str__(self):
        return f'{self.questionset} / {self.question} [{self.order}]'

    @property
    def element(self):
        return self.question
