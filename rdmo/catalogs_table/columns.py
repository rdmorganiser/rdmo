from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .utils import get_language_field_name

class LockedColumn(tables.Column):
    
    def render(self, value, record):
        ''' renders a toggle button for the locked state '''
        
        template_name = 'catalogs_table/columns/locked.html'

        context = {
                'locked': value,
                'pk' : str(record.pk),
                }
        return format_html(render_to_string(template_name, context))


class AvailableColumn(tables.Column):
    
    _template_name = 'catalogs_table/columns/available.html'
    
    def render(self, value, record):
        ''' renders a toggle button for the available state '''
        
        
        context = {
                'available': value,
                'pk' : str(record.pk),
                }
        rendered = render_to_string(self._template_name,context)
        
        return format_html(rendered)


class TitleColumn(tables.Column):
    
    _template_name  = 'catalogs_table/columns/title.html'

    def render(self, value, record):
        ''' renders the title as a link to the catalog detail view '''
        
        context = {
                'title': value,
                'record' : record,                 
                }
        return format_html(render_to_string(self._template_name, context))

    def order(self, queryset, is_descending):
        ''' orders the title by the field of current language '''
        
        title_lang_field = get_language_field_name('title')
        queryset = queryset.order_by(("-" if is_descending else "") + title_lang_field)
        return (queryset, True)


class SitesColumn(tables.Column):
    
    _template_name = 'catalogs_table/columns/sites.html'

    def render(self, value, record):
        ''' render the sites column with a str join of values in the sites attribute '''

        context = {'pk' : str(record.pk)}
        
        return format_html(render_to_string(self._template_name, context))
    
    def order(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")        
        return (queryset, True)


class OrderColumn(tables.Column):
    
    _template_name = 'catalogs_table/columns/order.html'

    def render(self, value, record):
        
        return format_html(render_to_string(self._template_name, {'order' : value}))

