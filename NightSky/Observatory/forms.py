from django import forms


class DirectoryForm(forms.Form):
    directory_path = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Directory path',
                                                                   'id': 'directory_path',
                                                                   'name': 'directory_path',
                                                                   'type': 'text'}),
                                     required=True)
