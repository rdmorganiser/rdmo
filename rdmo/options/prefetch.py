from django.db.models import Prefetch


def optionset_options_prefetch(lookup):
    from .models import OptionSetOption

    return Prefetch(lookup, queryset=OptionSetOption.objects.select_related('option'))
