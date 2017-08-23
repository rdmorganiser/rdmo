from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template

from rdmo.core.utils import get_uri_prefix
from rdmo.core.models import TranslationMixin
from rdmo.domain.models import AttributeEntity
from rdmo.conditions.models import Condition

from .validators import ViewUniqueKeyValidator


@python_2_unicode_compatible
class View(models.Model, TranslationMixin):

    uri = models.URLField(
        max_length=640, blank=True, null=True,
        verbose_name=_('URI'),
        help_text=_('The Uniform Resource Identifier of this view (auto-generated).')
    )
    uri_prefix = models.URLField(
        max_length=256, blank=True, null=True,
        verbose_name=_('URI Prefix'),
        help_text=_('The prefix for the URI of this view.')
    )
    key = models.SlugField(
        max_length=128, blank=True, null=True,
        verbose_name=_('Key'),
        help_text=_('The internal identifier of this view.')
    )
    comment = models.TextField(
        blank=True, null=True,
        verbose_name=_('Comment'),
        help_text=_('Additional internal information about this view.')
    )
    template = models.TextField(
        blank=True, null=True,
        verbose_name=_('Template'),
        help_text=_('The template for this view, written in Django template language.')
    )
    title_en = models.CharField(
        max_length=256, null=True, blank=True,
        verbose_name=_('Title (en)'),
        help_text=_('The English title for this view.')
    )
    title_de = models.CharField(
        max_length=256, null=True, blank=True,
        verbose_name=_('Title (de)'),
        help_text=_('The German title for this view.')
    )
    help_en = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (en)'),
        help_text=_('The English help text for this view.')
    )
    help_de = models.TextField(
        null=True, blank=True,
        verbose_name=_('Help (de)'),
        help_text=_('The German help text for this view.')
    )

    class Meta:
        ordering = ('key', )
        verbose_name = _('View')
        verbose_name_plural = _('Views')
        permissions = (('view_view', 'Can view View'),)

    def __str__(self):
        return self.uri or self.key

    def save(self, *args, **kwargs):
        self.uri = self.build_uri()
        super(View, self).save(*args, **kwargs)

    def clean(self):
        ViewUniqueKeyValidator(self).validate()

    @property
    def title(self):
        return self.trans('title')

    @property
    def help(self):
        return self.trans('help')

    def build_uri(self):
        return get_uri_prefix(self) + '/views/' + self.key

    def render(self, project, snapshot=None):
        # get list of conditions
        conditions = {}
        for condition in Condition.objects.all():
            conditions[condition.key] = condition.resolve(project, snapshot)

        # get the tree of entities
        entity_trees = AttributeEntity.objects.get_cached_trees()

        # get all values for this snapshot and put them in a dict labled by the values attibute id
        self.values_dict = {}
        self.set_index_dict = {}
        for value in project.values.filter(snapshot=snapshot):
            if value.attribute:
                # create entry for this values attribute in the values_dict
                if value.attribute.id not in self.values_dict:
                    self.values_dict[value.attribute.id] = []

                # add this value to the values_dict
                self.values_dict[value.attribute.id].append(value)

                # check if this values attribute has a parent collection
                if value.attribute.parent_collection:
                    # create entry for the parent collection in the set_index_dict
                    if value.attribute.parent_collection.id not in self.set_index_dict:
                        self.set_index_dict[value.attribute.parent_collection.id] = []

                    # add this values set_index tto the set_index_dict
                    if value.set_index not in self.set_index_dict[value.attribute.parent_collection.id]:
                        # print value.set_index
                        self.set_index_dict[value.attribute.parent_collection.id].append(value.set_index)

        # construct attribute/values tree from the input entity_trees using recursion
        values_tree = {}
        for entity_tree in entity_trees:
            values_tree[entity_tree.key] = self._build_values_tree(entity_tree)

        # render the template to a html string
        return Template(self.template).render(Context({
            'conditions': conditions,
            'values': values_tree
        }))

    def _build_values_tree(self, entity_tree_node, set_index=None):

        # check if this node is a collection entity or if the set_index is already set
        if entity_tree_node.is_collection and not entity_tree_node.is_attribute and set_index is None:
            node = []

            # loop over the set from the set_index_dict and call the current recursion step again,
            # but with the set_index set.
            if entity_tree_node.id in self.set_index_dict:
                for set_index in self.set_index_dict[entity_tree_node.id]:
                    node.append(self._build_values_tree(entity_tree_node, set_index))

            # return the list of set sub trees
            return node

        else:
            node = {}

            # use mptt's get_children() to walk the tree
            for child in entity_tree_node.get_children():

                if child.is_attribute:
                    # for an attribute look for values for this attribute in the values_dict
                    if child.id in self.values_dict:
                        # sort the values by their collection_index
                        sorted_values = sorted(self.values_dict[child.id], key=lambda x: x.collection_index)

                        # create a node_values list and loop over values to fill it
                        node_values = []
                        for value in sorted_values:
                            # append the value only if not set_index is set (for attributes without parent_attribute)
                            # or when the value's set_index matches the set_index set further up in the recursion
                            if set_index is None or value.set_index == set_index:
                                node_values.append(value.value)

                        if node_values:
                            # flatten the list if it is not a collection and append a the node for this attribute
                            if child.is_collection:
                                node[child.key] = node_values
                            else:
                                node[child.key] = node_values[0]

                else:
                    # for an entity proceed with the recursion
                    node[child.key] = self._build_values_tree(child, set_index)

            return node
