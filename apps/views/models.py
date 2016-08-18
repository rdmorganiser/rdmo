from __future__ import unicode_literals

from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template

from apps.domain.models import AttributeEntity


@python_2_unicode_compatible
class View(models.Model):

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    template = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _('View')
        verbose_name_plural = _('Views')

    def __str__(self):
        return self.title

    def render(self, snapshot):
        # get the tree of entities
        entity_trees = AttributeEntity.objects.get_cached_trees()

        # get all values for this snapshot and put them in a dict labled by the values attibute id
        self.values_dict = {}
        self.set_index_dict = {}
        for value in snapshot.values.all():
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
            values_tree[entity_tree.title] = self._build_values_tree(entity_tree)

        # render the template to a html string
        return Template(self.template).render(Context(values_tree))

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

                        # loop over values and append to the node for this attribute
                        node[child.title] = []
                        for value in sorted_values:
                            # append the value only if not set_index is set (for attributes without parent_attribute)
                            # or when the value's set_index matches the set_index set further up in the recursion
                            if set_index is None or value.set_index == set_index:
                                node[child.title].append(value.value)

                        # flatten the list if it has only one element
                        if len(node[child.title]) == 1:
                            node[child.title] = node[child.title][0]

                else:
                    # for an entity proceed with the recursion
                    node[child.title] = self._build_values_tree(child, set_index)

            return node
