from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from rdmo.core.models import Model
from rdmo.questions.models import Catalog, Question
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..managers import ProjectManager


class Project(Model):

    objects = ProjectManager()

    user = models.ManyToManyField(
        User, through='Membership',
        verbose_name=_('User'),
        help_text=_('The list of users for this project.')
    )
    site = models.ForeignKey(
        Site, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Site'),
        help_text=_('The site this project belongs to (in a multi site setup).')
    )
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'),
        help_text=_('The title for this project.')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('A description for this project (optional).')
    )
    catalog = models.ForeignKey(
        Catalog, related_name='projects', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Catalog'),
        help_text=_('The catalog which will be used for this project.')
    )
    tasks = models.ManyToManyField(
        Task, blank=True, through='Issue',
        verbose_name=_('Tasks'),
        help_text=_('The tasks that will be used for this project.')
    )
    views = models.ManyToManyField(
        View, blank=True,
        verbose_name=_('Views'),
        help_text=_('The views that will be used for this project.')
    )

    class Meta:
        ordering = ('title', )
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    @property
    def progress(self):
        total = Question.objects.filter(questionset__section__catalog=self.catalog) \
                                .distinct().values('attribute').count()
        values = self.values.filter(snapshot=None) \
                            .exclude(attribute__key='id') \
                            .exclude((models.Q(text='') | models.Q(text=None)) & models.Q(option=None)) \
                            .distinct().values('attribute').count()

        return {
            'total': total,
            'values': values,
            'ratio': values / total
        }

    @cached_property
    def member(self):
        return self.user.all()

    @cached_property
    def owners_str(self):
        return ', '.join(['' if x is None else str(x) for x in self.user.filter(membership__role='owner')])

    @cached_property
    def owners(self):
        return self.user.filter(membership__role='owner')

    @cached_property
    def managers(self):
        return self.user.filter(membership__role='manager')

    @cached_property
    def authors(self):
        return self.user.filter(membership__role='author')

    @cached_property
    def guests(self):
        return self.user.filter(membership__role='guest')
