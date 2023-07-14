from django_filters import CharFilter, FilterSet, ModelChoiceFilter
from rest_framework.filters import BaseFilterBackend

from rdmo.questions.models import Catalog

from .models import Project


def catalogs_for_user(request):
    if request is None:
        return Catalog.objects.none()

    catalogs = Catalog.objects.filter_current_site() \
            .filter_group(request.user) \
            .filter_availability(request.user)
    return catalogs


class ProjectFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    catalog = ModelChoiceFilter(queryset=catalogs_for_user)
    class Meta:
        model = Project
        fields = ('title', 'catalog')




class SnapshotFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if view.detail:
            return queryset

        snapshot = request.GET.get('snapshot')
        if snapshot:
            try:
                snapshot_pk = int(snapshot)
            except (ValueError, TypeError):
                snapshot_pk = None

            queryset = queryset.filter(snapshot__pk=snapshot_pk)
        else:
            queryset = queryset.filter(snapshot=None)

        return queryset


class ValueFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if view.detail:
            return queryset

        attributes = [int(attribute) for attribute in request.GET.getlist('attribute') if attribute.isdigit()]
        if attributes:
            queryset = queryset.filter(attribute__in=attributes)

        return queryset
