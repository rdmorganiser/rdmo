from django.contrib.auth import get_user_model

from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission, HasObjectPermission

from .serializers.v1 import UserSerializer
from .utils import is_site_manager


class UserViewSetMixin:

    def get_users_for_user(self, user):
        if user.is_authenticated:
            if user.has_perm('auth.view_user'):
                return get_user_model().objects.all()
            elif is_site_manager(user):
                return get_user_model().objects.filter(role__member__id__in=user.role.manager.all()).distinct()
        return get_user_model().objects.none()


class UserViewSet(UserViewSetMixin, ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission | HasObjectPermission, )
    serializer_class = UserSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'groups',
    )

    def get_queryset(self):
        return self.get_users_for_user(self.request.user) \
                   .prefetch_related('groups',
                                     'role__member', 'role__manager',
                                     'role__editor', 'role__reviewer',
                                     'memberships')
