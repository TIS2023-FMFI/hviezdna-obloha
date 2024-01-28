import django.db.utils
from django.db import connection
from django.shortcuts import render, redirect

from .forms import DirectoryForm, ExportForm
from .models import FitsImage
from .scripts.parsing import Parsing


def home(request):
    nights = number_of_nights(request)
    frames = number_of_frames(request)
    last_light_frame = last_light_frames_night(request)
    calib_frames = last_calib_frames_night(request)
    ccd_temp = last_ccd_temperature(request)

    context = {
        "nights": nights,
        "frames": frames,
        "last_light_frame": last_light_frame,
        "calib_frames": calib_frames,
        "ccd_temp": ccd_temp,
    }
    return render(request, "Observatory/home.html", context)


def import_fits(request):
    result = ""

    if request.method == "POST":
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory_path = form.cleaned_data["directory_path"]
            directory_path = "D:/TIS/20230503/" + directory_path[15:]  # change to your path to fits images instead of 'D:/'
            parsing = Parsing(directory_path)
            result = execute_query(str(parsing))
    else:
        form = DirectoryForm()

    return render(request, "Observatory/import_fits.html", {"form": form, "result": result})


def export_fits(request):  # TODO: REMOVE PRINTS
    if request.method == "POST":
        form = ExportForm(request.POST)
        print(form.data)

        if form.is_valid():
            fit = form.save(commit=False)
            print(fit)
            FitsImage.objects.filter()

            return redirect("export_fits")

    else:
        form = ExportForm()

    return render(request, "Observatory/export_fits.html", {"form": form})


def execute_query(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            return "DONE"
        except django.db.utils.IntegrityError:
            return "Already in database"


def number_of_nights(request):
    if FitsImage.objects.exists():
        nights = FitsImage.objects.values("DATE_OBS").distinct().count()
        return nights
    else:
        return 0

def number_of_frames(request):
    if FitsImage.objects.exists():
        frames = FitsImage.objects.latest("ID").ID
        return frames
    else:
        return 0

def last_light_frames_night(request):
    if FitsImage.objects.filter(IMAGETYP="LIGHT").exists():
        light_frames = FitsImage.objects.filter(IMAGETYP="LIGHT").latest("ID").DATE_OBS
        return light_frames
    else:
        return 0

def last_calib_frames_night(request):
    if FitsImage.objects.filter(IMAGETYP="CALIB").exists():
        calib_frames = FitsImage.objects.filter(IMAGETYP="CALIB").latest("ID").DATE_OBS
        return calib_frames
    else:
        return 0

def last_ccd_temperature(request):
    if FitsImage.objects.exists():
        last_fits_image = FitsImage.objects.latest("ID")
        ccd_temp = last_fits_image.CCD_TEMP
        return ccd_temp
    else:
        return 0
