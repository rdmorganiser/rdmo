
from django.conf import settings
from django.contrib.sites.models import Site

from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.template.loader import render_to_string
from rdmo.questions.models import Catalog

from rdmo.catalogs_table.utils import get_language_field_name
import django_tables2 as tables


class LockedColumn(tables.Column):
    
     def render(self, value, record):

        rendered = render_to_string('catalogs_table/columns/locked.html', 
                                    {'locked': value,
                                    'pk' : str(record.pk),
                                    'locked_form_url' : reverse('column_locked_form', args=str(record.pk))
                                    })
        
        return format_html(rendered)


class AvailableColumn(tables.Column):
    
     def render(self, value, record):

        rendered = render_to_string('catalogs_table/columns/available.html', 
                                    {'available': value,
                                    'pk' : str(record.pk),
                                    'available_form_url' : reverse('column_available_form', args=str(record.pk))
                                    })
        
        return format_html(rendered)


class TitleColumn(tables.Column):

    def render(self, value, record):
        ''' links the title to the catalogs page '''

        rendered = render_to_string('catalogs_table/columns/title.html', 
                                    {'value': value,
                                    'record' : record,                 
                                    'catalog_url' : reverse('catalogs') + str(record.pk),
                                    })
        return format_html(rendered)

    def order(self, queryset, is_descending):
        ''' orders the title by the field of current language '''
        
        title_lang_field = get_language_field_name('title')
        queryset = queryset.order_by(("-" if is_descending else "") + title_lang_field)
        return (queryset, True)

class SitesColumn(tables.Column):

    def render(self, value, record):
        ''' render the sites column with a str join of values in the sites attribute '''

        context = {
                    'sites': value.values(),
                    'sites_form_url' : reverse('column_sites_form', args=str(record.pk)),
                    'len_all_sites' : len(Site.objects.all()),
                    'pk' : str(record.pk)
                    }
        rendered = render_to_string('catalogs_table/columns/sites.html', context)
        return format_html(rendered)
    
    def order(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")        
        return (queryset, True)

class OrderColumn(tables.Column):

    def render(self, value, record):
        order =f'<code class="code-order">{value}</code>'
        return format_html(order)

class CatalogsTable(tables.Table):
    # TODO check column width with attrs

    title = TitleColumn(verbose_name = _("Catalog")) #, order_by = ("title_lang1", "title_lang2")
    
    updated = tables.DateTimeColumn(verbose_name = _("updated"), format='d.m.Y')
    created = tables.DateTimeColumn(verbose_name = _("created"), format='d.m.Y')
    
    available = AvailableColumn(verbose_name = _("Available"))
    locked = LockedColumn(verbose_name = _("Locked"))
    
    if settings.MULTISITE:
        sites = SitesColumn()
        sites_count = tables.Column()
    
    projects_count = tables.Column(verbose_name = _("Projects"))
    order = OrderColumn()
    
    class Meta:
        model = Catalog
        # template_name = "django_tables2/bootstrap4.html"
        template_name = "catalogs_table/tables_wrapper.html"
        # attrs = {"class": "table catalogs-table"}
        
        include = ('title', 'updated', 'created', 'available', 'locked',
                   'sites', 'projects_count', 'order')

        sequence = ('title', 'updated', 'available',  
                    'locked','sites','sites_count', 'projects_count', 'order', 'created')
        
        exclude = ('id', 'key','uri', 'comment', 'title_lang1', 'title_lang2', 'title_lang3', 'title_lang4',
                   'title_lang5', 'help_lang1', 'help_lang2', 'help_lang3', 'help_lang4',
                   'help_lang5', 'sites_count', 'uri_prefix', 'update' )
        
        empty_text = 'There are no catalogs available for this table'  
        # order_by = ('-updated')
