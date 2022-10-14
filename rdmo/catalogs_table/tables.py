from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from rdmo.catalogs_table.utils import get_language_field_name
from rdmo.questions.models import Catalog

import django_tables2 as tables

class LockedColumn(tables.Column):
    
    def render(self, value, record):
        ''' renders a toggle button for the locked state '''
        
        template_name = 'catalogs_table/columns/locked.html'

        context = {
                    'locked': value,
                    'pk' : str(record.pk),
                    'locked_form_url' : reverse('column_locked_form', args=str(record.pk)),
                }
        return format_html(render_to_string(template_name, context))


class AvailableColumn(tables.Column):
    
    def render(self, value, record):
        ''' renders a toggle button for the available state '''
        
        template_name = 'catalogs_table/columns/available.html'
        context = {
                    'available': value,
                    'pk' : str(record.pk),
                    'available_form_url' : reverse('column_available_form', args=str(record.pk)),
                }
        rendered = render_to_string(template_name,context)
        
        return format_html(rendered)


class TitleColumn(tables.Column):

    def render(self, value, record):
        ''' renders the title as a link to the catalog detail view '''
        
        template_name  = 'catalogs_table/columns/title.html'
        context = {
                    'value': value,
                    'record' : record,                 
                    'catalog_url' : reverse('catalogs') + str(record.pk),
                }
        return format_html(render_to_string(template_name, context))

    def order(self, queryset, is_descending):
        ''' orders the title by the field of current language '''
        
        title_lang_field = get_language_field_name('title')
        queryset = queryset.order_by(("-" if is_descending else "") + title_lang_field)
        return (queryset, True)


class SitesColumn(tables.Column):

    def render(self, value, record):
        ''' render the sites column with a str join of values in the sites attribute '''

        template_name = 'catalogs_table/columns/sites.html'
        context = {
                    'sites': value.values(),
                    'sites_form_url' : reverse('column_sites_form', args=str(record.pk)),
                    'all_sites' : Site.objects.count() == value.count(),
                    'pk' : str(record.pk)
                }
        return format_html(render_to_string(template_name, context))
    
    def order(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")        
        return (queryset, True)


class OrderColumn(tables.Column):

    def render(self, value, record):
        order =f'<code class="code-order">{value}</code>'
        return format_html(order)


class CatalogsTable(tables.Table):

    title = TitleColumn(verbose_name = _("Catalog"))
    
    updated = tables.DateTimeColumn(verbose_name = _("updated"), format='d.m.Y')
    created = tables.DateTimeColumn(verbose_name = _("created"), format='d.m.Y')
    
    available = AvailableColumn(verbose_name = _("Available"), attrs={
                                                        'td': {
                                                                'class': 'panel-default  text-center align-middle'
                                                                },
                                                        'th': {
                                                                'class' : 'text-center align-middle'
                                                                },
                                                        })
    locked = LockedColumn(verbose_name = _("Locked"), attrs={
                                                        'td': {
                                                                'class': 'panel-default  text-center align-middle'
                                                            },
                                                        })

    sites = SitesColumn(verbose_name = _("Sites"))
    
    projects_count = tables.Column(verbose_name = _("Projects"), attrs={
                                                        'td': {
                                                            'class': 'panel-default  text-center align-middle'
                                                            }
                                                        })
    order = OrderColumn( attrs={
                        'td': {
                            'class': 'panel-default  text-center align-middle'
                            }
                        })
    
    class Meta:
        model = Catalog
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
                'class' : ' panel panel-default panel-sites',
                'data-id' : lambda record: record.pk,
                }
        
        include = ('title', 'updated', 'created', 'available', 'locked',
                   'sites', 'projects_count', 'order')

        sequence = ('title', 'available', 'locked', 'sites',
                    'updated', 'projects_count', 'order', 'created')
        
        exclude = ('id', 'key','uri', 'comment', 'title_lang1', 'title_lang2',
                   'title_lang3', 'title_lang4', 'title_lang5', 'help_lang1', 'help_lang2',
                   'help_lang3', 'help_lang4','help_lang5', 'uri_prefix', 'update' )
        
        empty_text = _("There are no catalogs available for this table")
