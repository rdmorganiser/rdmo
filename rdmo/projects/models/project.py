from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from rdmo.conditions.models import Condition
from rdmo.core.constants import VALUE_TYPE_DATETIME, VALUE_TYPE_TEXT
from rdmo.core.models import Model
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..managers import ProjectManager
from .value import Value


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
        Catalog, related_name='+', on_delete=models.SET_NULL, null=True,
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

    def get_view_conditions(self, snapshot=None):
        conditions = {}
        for condition in Condition.objects.all():
            conditions[condition.key] = condition.resolve(self, snapshot)

        return conditions

    def get_view_values(self, snapshot=None):
        # get all values for this snapshot and put them in a dict labled by the values attibute path
        values = {
            'project/title': [[Value(text=self.title, value_type=VALUE_TYPE_TEXT)]],
            'project/description': [[Value(text=self.description, value_type=VALUE_TYPE_TEXT)]],
            'project/created': [[Value(text=self.created, value_type=VALUE_TYPE_DATETIME)]],
            'project/updated': [[Value(text=self.updated, value_type=VALUE_TYPE_DATETIME)]],
        }

        for value in self.values.filter(snapshot=snapshot):
            if value.attribute:
                attribute_path = value.attribute.path
                set_index = value.set_index

                # create entry for this values attribute in the values_dict
                if attribute_path not in values:
                    values[attribute_path] = []

                # add this value to the values
                try:
                    values[attribute_path][set_index].append(value)
                except IndexError:
                    values[attribute_path].append([value])

        return values
