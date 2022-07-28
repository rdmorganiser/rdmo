from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.template.loader import render_to_string
from rdmo.catalogs_table.forms import render_column_sites
from rdmo.questions.models import Catalog

from rdmo.catalogs_table.utils import wrap_uri, get_language_field_name
import django_tables2 as tables


class URIPrefixColumn(tables.Column):

    def render(self, value, record):
        ''' render the uri_prefix column with a split on . and a break in long strings '''

        wrapped_uri = wrap_uri(value)
        return format_html(wrapped_uri)

class UpdateColumn(tables.Column):

    def render(self, value, record):
        ''' adds a button to open a modal form '''

        update_form_url = reverse('column_update_form', args=str(record.pk))
        context= {'update_form_url': update_form_url}
        rendered = render_to_string('catalogs_table/columns/update.html', context)
        # button = f'<button class="btn btn-primary btn-sm" hx-get={update_form_url} hx-target="#dialog">Edit</button>'
        return format_html(rendered)



class LockedColumn(tables.Column):
    
     def render(self, value, record):

        # locked_form_url = 
        # TODO add this render function to view
        # rendered = CatalogsLockedFormView.render_to_string()
        rendered = render_to_string('catalogs_table/columns/locked.html', 
                                    {'locked': value,
                                    'pk' : str(record.pk),
                                    'locked_form_url' : reverse('column_locked_form', args=str(record.pk))
                                    })
        
        return format_html(rendered)

class AvailableColumn(tables.Column):
    
     def render(self, value, record):

        url= reverse('column_available_form', args=str(record.pk))
        # print(self, value,':', url)

        rendered = render_to_string('catalogs_table/columns/available.html', 
                                    {'available': value,
                                    'pk' : str(record.pk),
                                    'available_form_url' : reverse('column_available_form', args=str(record.pk))
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

        sites_form_url = reverse('column_sites_form', args=str(record.pk))        
        # TODO move this render function into a view
        # rendered = SitesListView._render_template_from_context(self.request, sites=None, sites_form_url=None, pk=None)
        context = {
                    'sites': value.values(),
                    'sites_form_url' : sites_form_url,
                    'pk' : str(record.pk)
                    }
        rendered = render_column_sites(context=context)
        # rendered = render_to_string('catalogs_table/columns/sites.html', 
        #                             )
        return format_html(rendered)
    
    def order(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")        
        return (queryset, True)

class CatalogsTable(tables.Table):
    # TODO check column width with attrs


    title = TitleColumn(verbose_name = _("Title")) #, order_by = ("title_lang1", "title_lang2")
    
    uri_prefix = URIPrefixColumn(verbose_name = _("URI Prefix"))
    # tables.Column(attrs = {"th":{"width": "10%;" }, "tf": {"bgcolor": "red"}})
    updated = tables.DateTimeColumn(verbose_name = _("updated"), format='d.m.Y G:i')
    created = tables.DateTimeColumn(verbose_name = _("created"), format='d.m.Y G:i')
    
    available = AvailableColumn(verbose_name = _("Available"))
    locked = LockedColumn(verbose_name = _("Locked"))
    sites = SitesColumn()
    sites_count = tables.Column()
    projects_count = tables.Column()
    update = UpdateColumn(verbose_name = _("Update catalog"), empty_values=(), orderable=False)
    
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
        # order_by = ('-updated')
