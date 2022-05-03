from django.utils.html import format_html

from rdmo.questions.models import Catalog

import django_tables2 as tables


class CatalogsTable(tables.Table):
    
    updated = tables.DateTimeColumn(format='d.m.Y G:i')
    created = tables.DateTimeColumn(format='d.m.Y G:i')
    projects_count = tables.Column()
    sites_count = tables.Column()
    sites = tables.Column()

    class Meta:
        model = Catalog
        template_name = "django_tables2/bootstrap.html"
        
        include = ('uri_prefix', 'updated','created', 'available', 'locked', 'title_lang1',
                   'sites', 'projects_count', 'sites_count')

        sequence = ('title_lang1', 'uri_prefix', 'created', 'updated', 'available',  
                    'locked','sites', 'projects_count', 'sites_count')
        
        exclude = ('key','uri', 'comment', 'title_lang2', 'title_lang3', 'title_lang4',
                   'title_lang5', 'help_lang1', 'help_lang2', 'help_lang3', 'help_lang4',
                   'help_lang5', 'id', 'order' )
        
        empty_text = 'There are no catalogs available for this table'  

    def render_uri_prefix(self, value, record):
        ''' render the uri_prefix column with a split on . and a break in long strings '''

        val_no_https = value.split('https://')[-1]
        if len(val_no_https.split('.')) >= 2:
            val_no_https_wbreak = val_no_https.split('.')[0] + '.' + '<br>'+ '.'.join(val_no_https.split('.')[1::])
        else:
            val_no_https_wbreak = val_no_https

        return format_html(val_no_https_wbreak)
    
    def render_sites(self, value):
        ''' render the sites column with a str join of values in the sites attribute '''

        sites = ", ".join(value.values_list('name',flat=True))
        
        return sites
    
    def order_sites(self, queryset, is_descending):
        ''' order the sites column with sites_count '''

        queryset = queryset.order_by(("-" if is_descending else "") + "sites_count")
        
        return (queryset, True)

