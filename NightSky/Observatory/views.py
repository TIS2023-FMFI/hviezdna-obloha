import django.db.utils
from django.db import connection
from django.shortcuts import render

from .forms import DirectoryForm, ExportForm
from .models import FitsImage
from .scripts.parsing import Parsing


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    result = ''

    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory_path = form.cleaned_data['directory_path']
            directory_path = 'D:/' + directory_path[15:]  # change to your path to fits images instead of 'D:/'
            parsing = Parsing(directory_path)
            result = execute_query(str(parsing))
    else:
        form = DirectoryForm()

    return render(request, 'Observatory/import_fits.html', {'form': form, 'result': result})


def export_fits(request):
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            # process form data
            pass
    else:
        form = ExportForm()

    return render(request, 'Observatory/export_fits.html', {'form': form})


def execute_query(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            return 'DONE'
        except django.db.utils.IntegrityError:
            return 'Already in database'


def number_of_nights(request):
    nights = FitsImage.objects.values('DATE_OBS').distinct().count()
    return render(request, 'Observatory/home.html', {'nights': nights})


def number_of_frames(request):
    frames = FitsImage.objects.latest('ID').ID
    return render(request, 'Observatory/home.html', {'frames': frames})


def last_light_frames_night(request):
    light_frames = FitsImage.objects.filter(IMAGETYP='light').latest('ID').DATE_OBS
    return render(request, 'Observatory/home.html', {'light_frames': light_frames})


def last_calib_frames_night(request):
    calib_frames = FitsImage.objects.filter(IMAGETYP='calib').latest('ID').DATE_OBS
    return render(request, 'Observatory/home.html', {'calib_frames': calib_frames})


def last_ccd_temperature(request):
    last_fits_image = FitsImage.objects.latest('ID')
    ccd_temp = last_fits_image.CCD_TEMP
    return render(request, 'Observatory/home.html', {'CCD_temp': ccd_temp})
