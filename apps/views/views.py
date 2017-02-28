from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.views import ModelPermissionMixin, ChoicesViewSet
from apps.core.utils import render_to_format
from apps.core.permissions import HasModelPermission

from .models import View
from .serializers import ViewSerializer, ViewIndexSerializer, ExportSerializer
from .renderers import XMLRenderer


class ViewsView(ModelPermissionMixin, TemplateView):
    template_name = 'views/views.html'
    permission_required = 'views.view_view'

    def get_context_data(self, **kwargs):
        context = super(ViewsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        return context


class ViewsExportView(ModelPermissionMixin, ListView):
    model = View
    context_object_name = 'views'
    permission_required = 'views.view_view'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['views'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="views.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Views'), 'views/views_export.html', context)


class ViewViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = View.objects.all()
    serializer_class = ViewSerializer

    @list_route()
    def index(self, request):
        queryset = View.objects.all()
        serializer = ViewIndexSerializer(queryset, many=True)
        return Response(serializer.data)
