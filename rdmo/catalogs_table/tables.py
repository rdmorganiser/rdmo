from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.template.loader import render_to_string
from rdmo.questions.models import Catalog

from rdmo.catalogs_table.utils import split_and_break_long_uri, get_language_field_name
import django_tables2 as tables


class LockedColumn(tables.Column):
    
     def render(self, value, record):

        catalog_update_locked_url = reverse('column_update_locked', args=str(record.pk))
        # TODO add this render function to view
        # rendered = CatalogsLockedFormView.render_to_string()
        rendered = render_to_string('catalogs_table/columns/locked.html', 
                                    {'locked': value,
                                    'update_locked_url' : catalog_update_locked_url
                                    })
        
        return format_html(rendered)

class TitleColumn(tables.Column):

    def render(self, value, record):
        ''' links the title to the catalogs page '''

        catalog_url = reverse('catalogs') + str(record.pk)
        catalog_url_link =f'<a href="{catalog_url}"><strong>{value}</strong></a>'
        return format_html(catalog_url_link)

    def order(self, queryset, is_descending):
        ''' orders the title by the field of current language '''
        title_lang_field = get_language_field_name('title')
        queryset = queryset.order_by(("-" if is_descending else "") + title_lang_field)
        return (queryset, True)


class SitesColumn(tables.Column):

    def render(self, value, record):
        ''' render the sites column with a str join of values in the sites attribute '''

        sites_form_url = reverse('column_update_sites', args=str(record.pk))        
        # TODO move this render function into a view
        # rendered = SitesListView._render_template_from_context(self.request, sites=None, sites_form_url=None, pk=None)
        rendered = render_to_string('catalogs_table/columns/sites.html', 
                                    {'sites': value.values(),
                                     'sites_form_url' : sites_form_url,
                                     'pk' : str(record.pk)
                                    })
        
        
        return format_html(rendered)
    
    def order(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")
        
        return (queryset, True)

class CatalogsTable(tables.Table):
    # TODO check column width with attrs
    title = TitleColumn(verbose_name = _("Title")) #, order_by = ("title_lang1", "title_lang2")
    
    uri_prefix = tables.Column(attrs = {"th":{"width": "10%;" },
                                        "tf": {"bgcolor": "red"}})
    updated = tables.DateTimeColumn(verbose_name = _("updated"), format='d.m.Y G:i')
    created = tables.DateTimeColumn(verbose_name = _("created"), format='d.m.Y G:i')
    
    locked = LockedColumn(verbose_name = _("Locked"))
    sites = SitesColumn()
    sites_count = tables.Column()
    projects_count = tables.Column()
    update = tables.Column(verbose_name = _("Update catalog"), empty_values=(), orderable=False)
    
    class Meta:
        model = Catalog
        # template_name = "django_tables2/bootstrap4.html"
        template_name = "catalogs_table/tables_wrapper.html"
        # attrs = {"class": "table catalogs-table"}
        
        include = ('id', 'title', 'uri_prefix', 'updated','created', 'available', 'locked',
                   'sites', 'projects_count', 'sites_count', 'order')

        sequence = ('id', 'title', 'uri_prefix', 'created', 'updated', 'available',  
                    'locked','sites','sites_count', 'projects_count', 'order', 'update' )
        
        exclude = ('key','uri', 'comment', 'title_lang1', 'title_lang2', 'title_lang3', 'title_lang4',
                   'title_lang5', 'help_lang1', 'help_lang2', 'help_lang3', 'help_lang4',
                   'help_lang5' )
        
        empty_text = 'There are no catalogs available for this table'  
        order_by = ('-updated')

    def render_uri_prefix(self, value, record):
        ''' render the uri_prefix column with a split on . and a break in long strings '''

        split_and_break_uri = split_and_break_long_uri(value)
        return format_html(split_and_break_uri)

    def render_update(self, value, record):

        catalog_update_url = reverse('catalog_update_modal', args=str(record.pk))
        button = f'<button class="btn btn-primary btn-sm" hx-get={catalog_update_url} hx-target="#dialog">Edit</button>'
        return format_html(button)
