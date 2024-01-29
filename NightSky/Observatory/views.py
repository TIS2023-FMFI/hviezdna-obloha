from .forms import DirectoryForm
from .forms import ExportForm
import django.db.utils
from django.shortcuts import render
from .scripts.parsing import Parsing
from .scripts.generate_sky_map import generate_sky_map
from django.db import connection
from .models import FITS_Image
from django.http import JsonResponse
import tkinter as tk
from tkinter import filedialog


def open_file_explorer(request):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # bring the window to the top
    directory_path = filedialog.askdirectory()
    root.destroy()
    return JsonResponse({'directory_path': directory_path})


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    result = ''
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory_path = form.cleaned_data['directory_path']
            p = Parsing(directory_path)
            result = execute_query(str(p))

            if result:
                generate_sky_map()
                result += " Sky coverage map has been updated."
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
    nights = FITS_Image.objects.values('DATE_OBS').distinct().count()
    return render(request, 'Observatory/home.html', {'nights': nights})


def number_of_frames(request):
    frames = FITS_Image.objects.latest('ID').ID
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
