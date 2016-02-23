from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from apps.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from .models import *


@login_required()
def domain(request):
    return render(request, 'domain/domain.html', {
        'attributes': Attribute.objects.all(),
        'attributesets': AttributeSet.objects.all()
    })


class AttributeCreateView(ProtectedCreateView):
    model = Attribute
    fields = '__all__'


class AttributeUpdateView(ProtectedUpdateView):
    model = Attribute
    fields = '__all__'


class AttributeDeleteView(ProtectedDeleteView):
    model = Attribute
    success_url = reverse_lazy('domain')


class AttributeSetCreateView(ProtectedCreateView):
    model = AttributeSet
    fields = '__all__'


class AttributeSetUpdateView(ProtectedUpdateView):
    model = AttributeSet
    fields = '__all__'


class AttributeSetDeleteView(ProtectedDeleteView):
    model = AttributeSet
    success_url = reverse_lazy('domain')
