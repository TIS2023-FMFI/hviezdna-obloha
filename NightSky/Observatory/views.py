import django.db.utils
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse

from .forms import DirectoryForm, ExportForm
from .models import FitsImage
from .scripts.first_insert import process_folders_with_fits
from .scripts.insert import Insert
from .scripts.create_log import Log
from .scripts.generate_sky_map import generate_sky_map

import tkinter as tk
from tkinter import filedialog


def open_file_explorer(request):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # bring the window to the top
    directory_path = filedialog.askdirectory()
    root.destroy()
    return JsonResponse({"directory_path": directory_path})


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
            # directory_path = 'D:/' + directory_path[15:] #change to your path to fits images instead of 'D:/'

            first_insert = False
            if first_insert:
                process_folders_with_fits(directory_path)
            else:
                # daily insert with generating log
                insert = Insert(directory_path)
                del insert
                log = Log(directory_path)
                log.generate_log()

            generate_sky_map()
            result += " Sky coverage map has been updated."

    else:
        form = DirectoryForm()

    return render(request, "Observatory/import_fits.html", {"form": form, "result": result})


def export_fits(request):  # TODO: REMOVE PRINTS
    if request.method == "POST":
        form = ExportForm(request.POST)
        # print(form.data)

        if form.is_valid():
            fits_image = form.save(commit=False)
            # print(fit)
            print(len(FitsImage.objects.filter()))

            return redirect("export_fits")

    else:
        form = ExportForm()

    return render(request, "Observatory/export_fits.html", {"form": form})


def number_of_nights(request):
    if FitsImage.objects.exists():
        nights = FitsImage.objects.values("DATE_OBS").distinct().count()
        return nights
    return 0


def number_of_frames(request):
    if FitsImage.objects.exists():
        frames = FitsImage.objects.latest("ID").ID
        return frames
    return 0


def last_light_frames_night(request):
    if FitsImage.objects.filter(IMAGETYP="LIGHT").exists():
        light_frames = FitsImage.objects.filter(IMAGETYP="LIGHT").latest("ID").DATE_OBS
        return light_frames
    return 0


def last_calib_frames_night(request):
    if FitsImage.objects.filter(IMAGETYP="CALIB").exists():
        calib_frames = FitsImage.objects.filter(IMAGETYP="CALIB").latest("ID").DATE_OBS
        return calib_frames
    return 0


def last_ccd_temperature(request):
    if FitsImage.objects.exists():
        last_fits_image = FitsImage.objects.latest("ID")
        ccd_temp = last_fits_image.CCD_TEMP
        return ccd_temp
    return 0
