from django import forms


class UploadFileForm(forms.Form):
    uploaded_file = forms.FileField(
        label='Select a file',
    )
