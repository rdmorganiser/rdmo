import logging

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView

from rdmo.core.views import ObjectPermissionMixin, RedirectViewMixin
from rdmo.questions.models import Catalog

from ..forms import ProjectForm
from ..models import Project
from ..utils import copy_project

logger = logging.getLogger(__name__)


class ProjectCopyView(ObjectPermissionMixin, RedirectViewMixin, UpdateView):

    model = Project
    form_class = ProjectForm
    permission_required = ('projects.add_project', 'projects.view_project_object')

    def get_form_kwargs(self):
        catalogs = Catalog.objects.filter_current_site() \
                                  .filter_group(self.request.user) \
                                  .filter_availability(self.request.user) \
                                  .order_by('-available', 'order')
        projects = Project.objects.filter_user(self.request.user)

        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'copy': True,
            'catalogs': catalogs,
            'projects': projects
        })
        return form_kwargs

    def form_valid(self, form):
        site = get_current_site(self.request)
        owners = [self.request.user]
        project = copy_project(form.instance, site, owners)
        return HttpResponseRedirect(project.get_absolute_url())
