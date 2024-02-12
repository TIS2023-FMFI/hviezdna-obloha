from django import forms
from .models import FitsImage


class DirectoryForm(forms.Form):
    directory_path = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Directory path", "id": "directory_path", "name": "directory_path", "type": "text"}
        ),
        required=True,
    )


class ExportForm(forms.ModelForm):
    class Meta:
        model = FitsImage
        exclude = ["PATH"]

