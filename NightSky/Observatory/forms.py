from django import forms


class DirectoryForm(forms.Form):
    directory_path = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-class', 'placeholder': 'File path'}),
                                     required=True)
