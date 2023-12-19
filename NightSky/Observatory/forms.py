from django import forms


class ImportFITSForm(forms.Form):
    directory_path = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter directory path containing '
                                                                                  'FITS files'}))
