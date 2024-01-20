from django import forms


class DirectoryForm(forms.Form):
    directory_path = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Directory path',
                                                                   'id': 'directory_path',
                                                                   'name': 'directory_path',
                                                                   'type': 'text'}),
                                     required=True)


class ExportForm(forms.Form):
    NAXIS = forms.BooleanField(label='Naxis', required=False)
    NAXIS1 = forms.BooleanField(label='Naxis1', required=False)
    NAXIS2 = forms.BooleanField(label='Naxis2', required=False)
    IMAGETYP = forms.BooleanField(label='Imagetype', required=False)
    FILTER = forms.BooleanField(label='Filter', required=False)
    OBJECT_NAME = forms.BooleanField(label='Object name', required=False)
    SERIES = forms.BooleanField(label='Series', required=False)
    NOTES = forms.BooleanField(label='Notes', required=False)
    DATE = forms.BooleanField(label='Date', required=False)
    MJD_OBS = forms.BooleanField(label='Mjd-obs', required=False)
    EXPTIME = forms.BooleanField(label='Exptime', required=False)
    CCD_TEMP = forms.BooleanField(label='Ccd-temp', required=False)
    XBINNING = forms.BooleanField(label='Xbinning', required=False)
    YBINNING = forms.BooleanField(label='Ybinning', required=False)
    XORGSUBF = forms.BooleanField(label='Xorgsubf', required=False)
    YORGSUBF = forms.BooleanField(label='Yorgsubf', required=False)
    MODE = forms.BooleanField(label='Mode', required=False)
    GAIN = forms.BooleanField(label='Gain', required=False)
    RD_NOISE = forms.BooleanField(label='Rd noise', required=False)
    OBSERVER = forms.BooleanField(label='Observer', required=False)
    RA = forms.BooleanField(label='Ra', required=False)
    DEC = forms.BooleanField(label='Dec', required=False)
    RA_PNT = forms.BooleanField(label='Ra pnt', required=False)
    DEC_PNT = forms.BooleanField(label='Dec pnt', required=False)
    AZIMUTH = forms.BooleanField(label='Azimuth', required=False)
    ELEVATIO = forms.BooleanField(label='Elevatio', required=False)
    AIRMASS = forms.BooleanField(label='Airmass', required=False)
    RATRACK = forms.BooleanField(label='Ratrack', required=False)
    DECTRACK = forms.BooleanField(label='Dectrack', required=False)
    PHASE = forms.BooleanField(label='Phase', required=False)
    RANGE = forms.BooleanField(label='Range', required=False)
