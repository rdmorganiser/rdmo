from django.db.models import Prefetch


def condition_prefetch(lookup):
    from .models import Condition

    return Prefetch(lookup, queryset=Condition.objects.select_related('source', 'target_option'))
