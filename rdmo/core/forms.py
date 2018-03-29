from django import forms


class UploadFileForm(forms.Form):
    uploaded_file = forms.FileField()
