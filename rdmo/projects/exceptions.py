from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException, NotFound

CATALOG_MISSING_DETAIL = _('This project has no catalog.')
CATALOG_MISSING_CODE = 'catalog_missing'


class CatalogMissingNotFound(NotFound):
    default_detail = CATALOG_MISSING_DETAIL
    default_code = CATALOG_MISSING_CODE


class CatalogMissingConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = CATALOG_MISSING_DETAIL
    default_code = CATALOG_MISSING_CODE
