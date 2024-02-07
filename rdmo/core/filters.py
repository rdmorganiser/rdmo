from django.db.models import Q
from django.utils.translation import get_language

from rest_framework.filters import BaseFilterBackend

from rdmo.core.utils import get_languages


class SearchFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if view.detail:
            return queryset

        search = request.GET.get('search')
        if search:
            q = Q()

            if 'uri' in view.search_fields:
                q |= Q(uri__contains=search)

            for lang_code, lang_string, lang_field in get_languages():
                if lang_code == get_language():
                    for search_field in ['title', 'text']:
                        if search_field in view.search_fields:
                            q |= Q(**{f'{search_field}_{lang_field}__contains': search})

            queryset = queryset.filter(q)

        return queryset
