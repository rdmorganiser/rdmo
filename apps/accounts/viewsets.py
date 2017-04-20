from django.contrib.auth.models import User

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from serializers.api import (
    UserSerializer as UserApiSerializer,
)


class UserApiViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = User.objects.all()
    serializer_class = UserApiSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_fields = (

    )
