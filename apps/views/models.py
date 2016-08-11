from __future__ import unicode_literals

from django.db import models

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template import Context, Template


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

    def render(self, entity_trees, snapshot):

        # get all values for this snapshot and put them in a dict labled by the values attibute id
        self.values_dict = {}
        for value in snapshot.values.all():
            if value.attribute.id not in self.values_dict:
                self.values_dict[value.attribute.id] = []
            self.values_dict[value.attribute.id].append(value)

        # construct attribute/values tree from the input entity_trees
        values_tree = {}
        for entity_tree in entity_trees:
            values_tree[entity_tree.title] = self._build_values_tree(entity_tree)

        # render the template to a html string
        return Template(self.template).render(Context(values_tree))

    def _build_values_tree(self, entity_tree_node):
        node = {}

        # use mptt's get_children() to walk the tree
        for child in entity_tree_node.get_children():
            if child.is_attribute:
                if child.id in self.values_dict:
                    if child.is_collection:
                        node[child.title] = [value.text for value in self.values_dict[child.id]]
                    else:
                        node[child.title] = self.values_dict[child.id][0].text
                else:
                    node[child.title] = None
            else:
                node[child.title] = self._build_values_tree(child)

        return node
