
from functools import reduce

from django.db.models import Q, Count
from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet, CharFilter

from rdmo.questions.models import Catalog

class CatalogsFilter(FilterSet):
    
    catalog = CharFilter( method='catalog_query', label=_("Title"))
    
    class Meta:
        model = Catalog
        fields = ('catalog',) # ['query', 'title', 'uri', 'comment', 'order', 'locked', 'available', 'sites']
    
    @property
    def qs(self):
        catalog_qs = super().qs
        return catalog_qs.annotate(
            projects_count=Count('projects', distinct=True), \
            sites_count=Count('sites',distinct=True))\
            .filter_group(self.request.user) \
            .filter_availability(self.request.user)

    
    def catalog_query(self, queryset, name, search_term, field_name='title'):
        title_fields = [i.name for i in Catalog._meta.get_fields() if i.name.startswith(field_name)]
        search_words = search_term.rstrip(' ').split(' ')
        
        if not search_term or not search_words:
            return queryset
        
        or_Q = [make_OR_query_fields(title_fields, word) for word in search_words]
        and_Q = reduce(lambda x, y: x & y, or_Q)
        
        return queryset.filter(and_Q)

    
def make_OR_query_fields(fields, value):
    or_Q = reduce(lambda x, y: x | y, [Q(**{f'{field}__icontains': value}) for field in fields])
    return or_Q
