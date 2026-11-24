from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class CatalogConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('This project has no catalog.')
    default_code = 'catalog_missing'
