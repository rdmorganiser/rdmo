from django.db.models import F, OuterRef, Q, Subquery
from django.db.models.functions import Concat
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter

from django_filters import CharFilter, FilterSet

from .models import Membership, Project


class ProjectFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ('title', 'catalog')


class ProjectSearchFilterBackend(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        if view.detail:
            return queryset

        search_terms = self.get_search_terms(request)
        if search_terms:
            for search_term in search_terms:
                queryset = queryset.filter(
                    Q(title__icontains=search_term) | (
                        Q(memberships__role='owner') & (
                            Q(memberships__user__username__icontains=search_term) |
                            Q(memberships__user__first_name__icontains=search_term) |
                            Q(memberships__user__last_name__icontains=search_term) |
                            Q(memberships__user__email__icontains=search_term)
                        )
                    )
                )

        return queryset


class ProjectDateFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if view.detail:
            return queryset

        created_before = self.parse_query_datetime(request, 'created_before')
        if created_before:
            queryset = queryset.filter(created__lte=created_before)

        created_after = self.parse_query_datetime(request, 'created_after')
        if created_after:
            queryset = queryset.filter(created__gte=created_after)

        updated_before = self.parse_query_datetime(request, 'updated_before')
        if updated_before:
            queryset = queryset.filter(updated__lte=updated_before)

        updated_after = self.parse_query_datetime(request, 'updated_after')
        if updated_after:
            queryset = queryset.filter(updated__gte=updated_after)

        last_changed_before = self.parse_query_datetime(request, 'last_changed_before')
        if last_changed_before:
            queryset = queryset.filter(last_changed__lte=last_changed_before)

        last_changed_after = self.parse_query_datetime(request, 'last_changed_after')
        if last_changed_after:
            queryset = queryset.filter(last_changed__gte=last_changed_after)

        return queryset

    def parse_query_datetime(self, request, key):
        value = request.GET.get(key)
        if value:
            datetime = parse_datetime(value)
            if datetime:
                if is_aware(datetime):
                    return datetime
                else:
                    return make_aware(datetime)


class ProjectOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        if view.detail:
            return queryset

        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if 'owner' in ordering or '-owner' in ordering:
                # annotate with the first owner, ordered by last_name, first_name
                owner_subquery = Subquery(
                    Membership.objects.filter(project=OuterRef('pk'), role='owner') \
                                      .annotate(owner=Concat(F('user__last_name'), F('user__first_name'))) \
                                      .order_by('owner') \
                                      [:1].values('owner')
                )
                queryset = queryset.annotate(owner=owner_subquery)

            elif 'progress' in ordering or '-progress' in ordering:
                # annotate with the progress ratio
                queryset = queryset.annotate(progress=(F('progress_count') + F('progress_total')))

            elif 'role' in ordering or '-role' in ordering:
                # annotate with the progress ratio
                role_subquery = Subquery(
                    Membership.objects.filter(project=OuterRef('pk'), user=request.user).values('role')
                )
                queryset = queryset.annotate(role=role_subquery)

            # order the queryset
            queryset = queryset.order_by(*ordering)

        return queryset


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
