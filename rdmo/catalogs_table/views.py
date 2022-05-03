from django.db import models
from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin

from rdmo.core.views import ModelPermissionMixin
from rdmo.questions.models import Catalog

from .tables import CatalogsTable
from django_tables2 import SingleTableView

class CatalogsTableView(ModelPermissionMixin, LoginRequiredMixin, SingleTableView):
        permission_required = 'questions.view_catalog'
        model = Catalog
        table_class = CatalogsTable
        table_data = Catalog.objects.annotate(projects_count=models.Count('projects', distinct=True), sites_count=models.Count('sites',distinct=True))
        template_name = 'catalogs_table/catalogs_table.html'
