from django import forms

from .models import Snapshot


class SnapshotForm(forms.ModelForm):

    class Meta:
        model = Snapshot
        fields = ('title', 'description')
