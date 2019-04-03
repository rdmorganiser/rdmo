from django.contrib.auth.models import User

from rest_framework.viewsets import ReadOnlyModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from rdmo.core.permissions import HasModelPermission

from .serializers.v1 import UserSerializer


class UserViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'username',
        'email',
        'project'
    )
