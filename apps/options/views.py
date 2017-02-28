from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.core.views import ModelPermissionMixin
from apps.core.utils import render_to_format
from apps.core.permissions import HasModelPermission

from apps.conditions.models import Condition

from .models import OptionSet, Option
from .serializers import (
    OptionSetIndexSerializer,
    OptionSetSerializer,
    OptionSerializer,
    ConditionSerializer,
    ExportSerializer
)
from .renderers import XMLRenderer


class OptionsView(ModelPermissionMixin, TemplateView):
    template_name = 'options/options.html'
    permission_required = 'options.view_option'

    def get_context_data(self, **kwargs):
        context = super(OptionsView, self).get_context_data(**kwargs)
        context['export_formats'] = settings.EXPORT_FORMATS
        return context


class OptionsExportView(ModelPermissionMixin, ListView):
    model = OptionSet
    context_object_name = 'optionsets'
    permission_required = 'options.view_option'

    def render_to_response(self, context, **response_kwargs):
        format = self.kwargs.get('format')
        if format == 'xml':
            serializer = ExportSerializer(context['optionsets'], many=True)
            response = HttpResponse(XMLRenderer().render(serializer.data), content_type="application/xml")
            response['Content-Disposition'] = 'filename="options.xml"'
            return response
        else:
            return render_to_format(self.request, format, _('Options'), 'options/options_export.html', context)


class OptionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer

    @list_route()
    def index(self, request):
        queryset = OptionSet.objects.all()
        serializer = OptionSetIndexSerializer(queryset, many=True)
        return Response(serializer.data)


class OptionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Option.objects.order_by('order')
    serializer_class = OptionSerializer


class ConditionViewSet(ReadOnlyModelViewSet):
    permission_classes = (HasModelPermission, )

    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
