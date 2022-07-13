import pdb
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from rdmo.questions.models import Catalog

from rdmo.catalogs_table.utils import split_and_break_long_uri, get_language_field_name
# from rdmo.catalogs_table.views.SitesListView import 
from rdmo.catalogs_table.forms import CatalogsLockedFormView
import django_tables2 as tables


class LockedColumn(tables.Column):
    
     def render(self, value, record):

        catalog_update_locked_url = reverse('table_update_locked', args=str(record.pk))
        
        # print(f'record {record}, value {value}')
        # button = '<button hx-post="/clicked" hx-swap="outerHTML">Click Me </button>
        # button = f'<button type="checkbox" hx-post={catalog_update_locked_url} hx-swap="this" hx-target="#dialog" ></button>'
        # checkbox = f'<input type="checkbox" name="locked_checkbox" value={str(1 if value else 0)}>'value="{value}"
        button = f'<class="checkbox" hx-trigger="load, catalogsChanged from:body" hx-get="{catalog_update_locked_url}">'
        catalog_update_locked_url = reverse('table_update_locked', args=str(record.pk))
        # pdb.set_trace()
        rendered = render_to_string('catalogs_table/columns/locked.html', 
                                    {'locked': value,
                                    'update_locked_url' : catalog_update_locked_url
                                    })
        # rendered = CatalogsLockedFormView.as_view()
        # button = f'<button class="btn btn-primary btn-checkbox" hx-trigger="load, catalogChanged from:body" hx-get={catalog_update_locked_url} hx-target="this"</button>'
        return format_html(rendered)

class TitleColumn(tables.Column):

    def render(self, value, record):

        catalog_url = reverse('catalogs') + str(record.pk)
        catalog_url_link =f'<a href="{catalog_url}"><strong>{value}</strong></a>'

        return format_html(catalog_url_link)

    def order(self, queryset, is_descending):
        print('\norder_title qs Called: ', queryset,'\n' )
        # print('order_ by field: ', self.order_by_field )
        # Catalog().trans()
        # TODO fixed but remove extra stuff
        # getlang = get_language()
        title_lang_field = get_language_field_name('title')
        print(f'\nPre-sort Title for lang: {title_lang_field}', "; ".join([i.title for i in queryset]),'\n')
        # pdb.set_trace()
        queryset = queryset.order_by(("-" if is_descending else "") + title_lang_field)
        print('Sort Title:', "; ".join([i.title for i in queryset]),'\n')
        return (queryset, True)

        # qs_sorted = sorted(queryset, key=lambda x:x.title, reverse=is_descending)
        
        # # queryset = queryset.order_by(("-" if is_descending else "") + "title")
        # # <CatalogQuestionSet
        
        # return (queryset, True)


'''
<div hx-target="this" hx-swap="outerHTML">
    <div><label>First Name</label>: Joe</div>
    <div><label>Last Name</label>: Blow</div>
    <div><label>Email</label>: joe@blow.com</div>
    <button hx-get="/contact/1/edit" class="btn btn-primary">
    Click To Edit
    </button>
</div>
'''



class SitesColumn(tables.Column):

    def render(self, value, record):
        ''' render the sites column with a str join of values in the sites attribute '''

        sites_values = value.values_list('name',flat=True)
        sites_values_li = "".join([f'<li>{i}</li>' for i in sites_values])
        sites_values_ul = '<ul>'+sites_values_li+'</ul>'
        sites_edit_div = f'<div class="table-row-sites-{str(record.pk)}" hx-target="this" hx-swap="outerHTML">'

        sites_form_url = reverse('table_update_sites', args=str(record.pk))
        # pdb.set_trace()
        catalog_list_sites_url = reverse('table_list_sites', args=str(record.pk))
        # TODO move this render function into a view
        rendered = render_to_string('catalogs_table/columns/sites.html', 
                                    {'sites': value.values(),
                                     'sites_form_url' : sites_form_url,
                                     'pk' : str(record.pk)
                                    })
        # rendered = SitesListView.render_template_from_context(self.request, sites=None, sites_form_url=None, pk=None)
        
        # sites_edit_button = f'<button hx-get="{sites_form_url}" class="btn btn-primary">Click To Edit</button>'
        # button = f'<class="checkbox" hx-trigger="load, catalogsChanged from:body" hx-get="{catalog_update_sites_url}" hx-target="this">'
        # sites_edit_div+sites_values_ul+sites_edit_button+'</div>'
        return format_html(rendered)
    
    def order(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")
        
        return (queryset, True)

class CatalogsTable(tables.Table):
    # TODO check width attrs
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
        # print(f'Value: {value}, split: {split_and_break_uri}')
        
        return format_html(split_and_break_uri)

    def render_update(self, value, record):

        catalog_update_url = reverse('table_update_catalog_modal', args=str(record.pk))
        # "{% url 'table_update_catalog_modal' 1 %}"
        button = f'<button class="btn btn-primary btn-sm" hx-get={catalog_update_url} hx-target="#dialog">Edit</button>'
        return format_html(button)


class _ModifyCatalogColumn(tables.Column):
    modify = tables.Column(empty_values=(),
                           orderable=False,
                           linkify=True)

