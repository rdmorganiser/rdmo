from rest_framework.filters import BaseFilterBackend

from rdmo.domain.models import Attribute


class ValueFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        set_attribute = request.GET.get('set_attribute')
        if set_attribute:
            try:
                attribute = Attribute.objects.get(pk=set_attribute)
                attributes = attribute.get_descendants(include_self=True).filter()
                queryset = queryset.filter(attribute__in=attributes)

            except Attribute.DoesNotExist:
                queryset = queryset.none()

        return queryset
