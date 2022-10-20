
from django.utils.translation import gettext_lazy as _

from rdmo.questions.models import Catalog

import django_tables2 as tables

from .columns import TitleColumn, AvailableColumn, LockedColumn, SitesColumn, OrderColumn

class CatalogsTable(tables.Table):

    title = TitleColumn(verbose_name = _("Catalog"), attrs= {
                                                            'td': {'class': 'table-title',
                                                                    'style' : 'max-width:400px; min-width:400px;',
                                                                    }
                                                             })
    
    updated = tables.DateTimeColumn(verbose_name = _("updated"), format='d.m.Y')
    created = tables.DateTimeColumn(verbose_name = _("created"), format='d.m.Y')
    
    available = AvailableColumn(verbose_name = _("Available"), attrs={
                                                        'td': {
                                                                'class': 'panel-default  text-center align-middle',
                                                                },
                                                        })
    locked = LockedColumn(verbose_name = _("Locked"), attrs={
                                                        'td': {
                                                                'class': 'panel-default  text-center align-middle',
                                                            },
                                                        })

    sites = SitesColumn(verbose_name = _("Sites"), attrs={
                                                        'td': {
                                                                'class': 'panel-default',
                                                                'style' : 'max-width:120px; min-width:120px;',
                                                            },
                                                        })
    
    projects_count = tables.Column(verbose_name = _("Projects"), attrs={
                                                        'td': {
                                                            'class': 'panel-default  text-center align-middle',
                                                            }
                                                        })
    order = OrderColumn( attrs={
                        'td': {
                            'class': 'panel-default  text-center align-middle'
                            }
                        })
    
    class Meta:
        model = Catalog
        row_attrs = {
                'class' : ' panel panel-default panel-sites',
                'data-id' : lambda record: record.pk,
                }
        attrs = {
            'th' : {
          'class' : 'text-center align-middle',
            }
        }
        per_page = 7
        
        include = ('title', 'updated', 'created', 'available', 'locked',
                   'sites', 'projects_count', 'order')

        sequence = ('title', 'available', 'locked', 'sites',
                    'updated', 'projects_count', 'order', 'created')
        
        exclude = ('id', 'key','uri', 'comment', 'title_lang1', 'title_lang2',
                   'title_lang3', 'title_lang4', 'title_lang5', 'help_lang1', 'help_lang2',
                   'help_lang3', 'help_lang4','help_lang5', 'uri_prefix', 'update' )
        
        empty_text = _("There are no catalogs available for this table")
