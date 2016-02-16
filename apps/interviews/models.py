from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from apps.projects.models import Project
from apps.questions.models import Question, Group


@python_2_unicode_compatible
class Interview(models.Model):

    project = models.ForeignKey(Project, related_name='interviews')

    title = models.CharField(max_length=256)

    completed = models.BooleanField()
    current_group = models.ForeignKey(Group, null=True, blank=True)

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()

        self.updated = now()
        super(Interview, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('project', 'updated')
        verbose_name = _('Interview')
        verbose_name_plural = _('Interviews')


@python_2_unicode_compatible
class Answer(models.Model):

    interview = models.ForeignKey('Interview', related_name='answers')
    question = models.ForeignKey(Question)
    value = models.TextField()

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField(editable=False)

    @property
    def text(self):
        if self.question.answer_type == 'bool':
            if self.value == '1':
                return _('yes')
            else:
                return _('no')
        else:
            return self.value

    @property
    def project_name(self):
        return self.interview.project.name

    @property
    def interview_title(self):
        return self.interview.title

    @property
    def section_slug(self):
        return self.question.group.subsection.section.slug

    @property
    def subsection_slug(self):
        return self.question.group.subsection.slug

    @property
    def group_slug(self):
        return self.question.group.slug

    @property
    def question_slug(self):
        return self.question.slug

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = now()

        self.updated = now()
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.question.slug

    class Meta:
        ordering = ('interview', 'question')
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
