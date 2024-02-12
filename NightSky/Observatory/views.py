import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta

from django.forms import MultipleChoiceField
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .forms import (
    DirectoryForm,
    ExportForm,
    MultipleIntegerIntervalsField,
    MultipleFloatIntervalsField,
    MultipleStringsField,
)
from .models import FitsImage
from .scripts.create_log import Log
from .scripts.first_insert import process_folders_with_fits
from .scripts.generate_sky_map import generate_sky_map
from .scripts.insert import Insert


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
    form = DirectoryForm(request.POST or None)
    path = r"C:\UNI\TIS"

    # Get the last added directory path in the archive
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    directories.sort(key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
    last_added_directory_path = os.path.join(path, directories[0]) if directories else None

    if request.method == "POST":
        if "import_last_night" in request.POST and last_added_directory_path:
            directory_path = last_added_directory_path
            success, message = process_and_log_directory(directory_path, request)
            if success:
                messages.success(request, message)
            else:
                messages.error(request, f"Import failed: {message}")
            request.session["form_submitted"] = "import_last_night"

        elif "import_directory" in request.POST:
            if form.is_valid():
                directory_path = form.cleaned_data["directory_path"]
                success, message = process_and_log_directory(directory_path, request)
                if success:
                    messages.success(request, message)
                else:
                    messages.error(request, f"Import failed: {message}")
            else:
                messages.error(request, "Incorrect input: Please ensure the directory path is correct.")
            request.session["form_submitted"] = "import_directory"

    return render(
        request, "Observatory/import_fits.html", {"form": form, "last_added_directory_path": last_added_directory_path}
    )


def process_and_log_directory(directory_path, request):
    try:
        first_insert = False
        if first_insert:
            process_folders_with_fits(directory_path)
        else:
            insert = Insert(directory_path)
            del insert
            log = Log(directory_path)
            log.generate_log()
        generate_sky_map()
        return True, "Import successful."
    except Exception as e:
        return False, str(e)


def filter_fits_images(form_data):
    ...
    # Entry.objects.values_list("id", flat=True).order_by("id")


def export_fits(request):  # TODO: REMOVE PRINTS
    if request.method == "POST":
        form = ExportForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            queryset = FitsImage.objects.all()

            for field_name, field in form.fields.items():
                field_input = form.cleaned_data.get(field_name)

                if not field_input:
                    continue

                if isinstance(field, MultipleIntegerIntervalsField):
                    exact_values, intervals = field_input
                    q_objects = Q(**{"%s__in" % field_name: exact_values + intervals})
                    queryset = queryset.filter(q_objects)

                if isinstance(field, MultipleFloatIntervalsField):
                    exact_values, intervals = field_input
                    q_objects = Q(**{"%s__in" % field_name: exact_values})

                    for left_endpoint, right_endpoint in intervals:
                        q_objects |= Q(**{"%s__range" % field_name: (left_endpoint, right_endpoint)})

                    queryset = queryset.filter(q_objects)

                if isinstance(field, (MultipleStringsField, MultipleChoiceField)):
                    q_objects = Q(**{"%s__in" % field_name: field_input})
                    queryset = queryset.filter(q_objects)

            paths = queryset.values_list("PATH", flat=True).order_by("PATH")

            print("---- PATHS ----")
            print(paths)
            print(len(paths), "\n--------")

            # fits_image = form.save(commit=False)
            # print(fits_image)
            # print(len(FitsImage.objects.filter(form.data)))

            return redirect("export_fits")

    else:
        form = ExportForm()

    return render(request, "Observatory/export_fits.html", {"form": form})


def number_of_nights(request):
    if FitsImage.objects.exists():
        date_obs_values = FitsImage.objects.values_list("DATE_OBS", flat=True)

        adjusted_dates = set()
        for date_obs in date_obs_values:
            date_time = datetime.strptime(date_obs, "%Y-%m-%dT%H:%M:%S.%f")

            if date_time.time() < datetime.strptime("12:00:00", "%H:%M:%S").time():
                date_time -= timedelta(days=1)
            adjusted_dates.add(date_time.date())

        return len(adjusted_dates)
    return None


def number_of_frames(request):
    if FitsImage.objects.exists():
        frames = FitsImage.objects.count()
        return frames
    return None


def last_light_frames_night(request):
    if FitsImage.objects.filter(IMAGETYP="LIGHT").exists():
        light_frames = FitsImage.objects.filter(IMAGETYP="LIGHT").latest("DATE_OBS").DATE_OBS
        return light_frames
    return None


def last_calib_frames_night(request):
    if FitsImage.objects.filter(IMAGETYP="CALIB").exists():
        calib_frames = FitsImage.objects.filter(IMAGETYP="CALIB").latest("DATE_OBS").DATE_OBS
        return calib_frames
    return None


def last_ccd_temperature(request):
    if FitsImage.objects.exists():
        last_fits_image = FitsImage.objects.latest("DATE_OBS")
        ccd_temp = last_fits_image.CCD_TEMP
        return ccd_temp
    return None
