import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Overlay

logger = logging.getLogger(__name__)


@login_required()
def reset_overlays(request):
    if request.method == 'POST':
        Overlay.objects.filter(user=request.user).delete()
        return redirect('projects')

    return render(request, 'overlays/reset_overlays.html')
