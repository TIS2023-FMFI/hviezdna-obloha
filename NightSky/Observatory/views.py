from .forms import DirectoryForm
import django.db.utils
from django.shortcuts import render
from .scripts.parsing import Parsing
from django.db import connection
from .models import FITS_Image


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    result = ''
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory_path = form.cleaned_data['directory_path']
            directory_path = 'C:/Users/anna4/Documents/20230503/' + directory_path[15:] #change to your path to fits images
            p = Parsing(directory_path)
            result = execute_query(str(p))
    else:
        form = DirectoryForm()
    return render(request, 'Observatory/import_fits.html', {'form': form, 'result': result})


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')


def execute_query(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            return 'DONE'
        except django.db.utils.IntegrityError:
            return 'Already in database'


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')


def number_of_nights(request):
    nights = FITS_Image.objects.values('DATE_OBS').distinct().count()
    return render(request, 'Observatory/home.html', {'nights': nights})

def number_of_frames(request):
    frames =  FITS_Image.objects.latest('ID').ID
    return render(request, 'Observatory/home.html', {'frames': frames})

def last_light_frames_night(request):
    light_frames = FITS_Image.objects.filter(IMAGETYP='light').latest('ID').DATE_OBS
    return render(request, 'Observatory/home.html', {'light_frames': light_frames})


def last_calib_frames_night(request):
    calib_frames = FITS_Image.objects.filter(IMAGETYP='calib').latest('ID').DATE_OBS
    return render(request, 'Observatory/home.html', {'calib_frames': calib_frames})


def last_CCD_temperature(request):
    last_fits_image = FITS_Image.objects.latest('ID')
    CCD_temp = last_fits_image.CCD_TEMP
    return render(request, 'Observatory/home.html', {'CCD_temp': CCD_temp})
