from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from rdmo.core.models import Model
from rdmo.questions.models import Catalog
from rdmo.tasks.models import Task
from rdmo.views.models import View

from ..managers import ProjectManager


class Project(MPTTModel, Model):

    objects = ProjectManager()

    parent = TreeForeignKey(
        'self', null=True, blank=True,
        on_delete=models.DO_NOTHING, related_name='children', db_index=True,
        verbose_name=_('Parent project'),
        help_text=_('The parent project of this project.')
    )
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Membership', related_name='projects',
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
        Task, blank=True, through='Issue', related_name='projects',
        verbose_name=_('Tasks'),
        help_text=_('The tasks that will be used for this project.')
    )
    views = models.ManyToManyField(
        View, blank=True, related_name='projects',
        verbose_name=_('Views'),
        help_text=_('The views that will be used for this project.')
    )
    progress_total = models.IntegerField(
        null=True,
        verbose_name=_('Progress total'),
        help_text=_('The total number of expected values for the progress bar.')
    )
    progress_count = models.IntegerField(
        null=True,
        verbose_name=_('Progress count'),
        help_text=_('The number of values for the progress bar.')
    )

    class Meta:
        ordering = ('tree_id', 'level', 'title')
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    class MPTTMeta:
        order_insertion_by = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project', kwargs={'pk': self.pk})

    def clean(self):
        if self.id and self.parent in self.get_descendants(include_self=True):
            raise ValidationError({
                'parent': [_('A project may not be moved to be a child of itself or one of its descendants.')]
            })

    @property
    def catalog_uri(self):
        if self.catalog is not None:
            return self.catalog.uri

    @cached_property
    def member(self):
        return self.user.all()

    @cached_property
    def owners_str(self):
        return ', '.join(['' if x is None else str(x) for x in self.user.filter(membership__role='owner')])

    @property
    def owners(self):
        return self.get_members('owner')

    @property
    def managers(self):
        return self.get_members('manager')

    @property
    def authors(self):
        return self.get_members('author')

    @property
    def guests(self):
        return self.get_members('guest')

    @property
    def file_size(self):
        queryset = self.values.filter(snapshot=None).exclude(models.Q(file='') | models.Q(file=None))
        return sum([value.file.size for value in queryset])

    def get_members(self, role):
        try:
            # membership_list is created by the Prefetch call in the viewset
            return [membership.user for membership in self.memberships_list if membership.role == role]
        except AttributeError:
            # membership_list does not exist
            return self.user.filter(memberships__role=role)


@receiver(pre_delete, sender=Project)
def reparent_children(sender, instance, **kwargs):
    for child in instance.get_children():
        child.move_to(instance.parent, 'last-child')
        child.save()
