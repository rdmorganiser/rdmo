from rest_framework.filters import BaseFilterBackend

from rdmo.domain.models import AttributeEntity


class ValueFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        set_entity = request.GET.get('set_entity')
        if set_entity:
            try:
                attribute_entity = AttributeEntity.objects.get(pk=set_entity)
                attributes = attribute_entity.get_descendants(include_self=True).filter()
                queryset = queryset.filter(attribute__in=attributes)

            except AttributeEntity.DoesNotExist:
                queryset = queryset.none()


        return queryset
