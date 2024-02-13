import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime, timedelta
import json
import shutil

import django.db.utils
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.forms import MultipleChoiceField

from .forms import (
    DirectoryForm,
    ExportForm,
    MultipleIntegerIntervalsField,
    MultipleFloatIntervalsField,
    MultipleStringsField,
)
from .models import FitsImage
from .scripts.first_insert import process_folders_with_fits
from .scripts.insert import Insert
from .scripts.create_log import Log
from .scripts.first_insert import process_folders_with_fits
from .scripts.generate_sky_map import generate_sky_map

from datetime import datetime, timedelta
import re


# home.html functions
def home(request):
    context = {
        "nights": number_of_nights(request),
        "frames": number_of_frames(request),
        "last_light_frame": last_light_frames_night(request),
        "calib_frames": last_calib_frames_night(request),
        "ccd_temp": last_ccd_temperature(request),
    }
    return render(request, "Observatory/home.html", context)


def number_of_nights(request):
    if FitsImage.objects.exists():
        date_obs_values = FitsImage.objects.values_list("DATE_OBS", flat=True)

        adjusted_dates = set()
        for date_obs in date_obs_values:
            if date_obs is not None:
                date_time = datetime.strptime(date_obs, "%Y-%m-%dT%H:%M:%S.%f")

                if date_time.time() < datetime.strptime("12:00:00", "%H:%M:%S").time():
                    date_time -= timedelta(days=1)
                adjusted_dates.add(date_time.date())
        return len(adjusted_dates)
    return None


def number_of_frames(request):
    return FitsImage.objects.count() if FitsImage.objects.exists() else None


def last_light_frames_night(request):
    return FitsImage.objects.filter(IMAGETYP="LIGHT").latest("DATE_OBS").DATE_OBS \
        if FitsImage.objects.filter(IMAGETYP="LIGHT").exists() else None


def last_calib_frames_night(request):
    return FitsImage.objects.filter(IMAGETYP="CALIB").latest("DATE_OBS").DATE_OBS \
        if FitsImage.objects.filter(IMAGETYP="CALIB").exists() else None


def last_ccd_temperature(request):
    return FitsImage.objects.latest("DATE_OBS").CCD_TEMP if FitsImage.objects.exists() else None


# import_fits.html functions
def import_fits(request):
    form = DirectoryForm(request.POST or None)
    path = r"C:"

    # Get the last added directory path in the archive
    last_added_directory_path = get_last_added_directory_path(path, request)

    if request.method == "POST":
        if "import_last_night" in request.POST and last_added_directory_path:
            directory_path = last_added_directory_path
            handle_import(directory_path, request, "import_last_night")

        elif "import_directory" in request.POST and form.is_valid():
            directory_path = form.cleaned_data["directory_path"]
            handle_import(directory_path, request, "import_directory")
        else:
            messages.error(request, "Incorrect input: Please ensure the directory path exists.")

    return render(
        request, "Observatory/import_fits.html", {"form": form, "last_added_directory_path": last_added_directory_path}
    )


def get_last_added_directory_path(path, request):
    try:
        directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        directories.sort(key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
    except Exception as e:
        messages.error(request, f"Failed to list directories: {str(e)}")
        directories = []
    request.session["form_submitted"] = "import_last_night"
    return os.path.join(path, directories[0]) if directories else None


def handle_import(directory_path, request, session_key):
    inserted_rows = process_and_log_directory(directory_path, request)
    if inserted_rows is not None:
        messages.success(request, f"Successfully imported {inserted_rows} FITS images.")
    request.session["form_submitted"] = session_key


def process_and_log_directory(directory_path, request):
    first_insert = False
    try:
        if first_insert:
            inserted_rows = process_folders_with_fits(directory_path)
        else:
            insert = Insert(directory_path)
            inserted_rows = insert.get_number_of_inserted_rows()

            if inserted_rows != 0:
                log = Log(insert.headers, directory_path)
                log.generate_log()
                del log

            del insert
        generate_sky_map()
        return inserted_rows
    except FileNotFoundError:
        messages.error(request, "Import failed. Directory does not exist.")
        return None


def open_file_explorer(request):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # bring the window to the top
    directory_path = filedialog.askdirectory()
    root.destroy()
    return JsonResponse({"directory_path": directory_path})


def filter_fits_images(form_data):
    ...
    # Entry.objects.values_list("id", flat=True).order_by("id")


def export_fits(request):  # TODO: REMOVE PRINTS
    results = None

    if request.method == "POST":
        form = ExportForm(request.POST)

        target_path = request.POST.get("target_directory_path")
        if target_path == "":
            return JsonResponse({"error_message": "No target directory selected!"})

        # SQL query form processing
        if request.POST.get("is_sql"):
            sql_input = add_quotes(request.POST.get("sql_input"))

            # TODO: check copying into inexisting folder
            try:
                if is_valid_sql_query(sql_input):
                    results = execute_sql_query(sql_input)
                    print(results)
                    # print([r[0] for r in results])
                    return JsonResponse({"source_paths": results, "target_path": target_path})

                else:
                    return JsonResponse({"error_message": "Wrong SQL query"})

            except Exception as e:
                return JsonResponse({"error_message": f"Error executing the SQL query: {e}"})

        # Export form processing
        elif form.is_valid():
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

            paths = queryset.values_list("PATH", flat=True)

            return JsonResponse({"source_paths": list(paths), "target_path": target_path})

        return redirect("export_fits")

    else:
        form = ExportForm()

    return render(request, "Observatory/export_fits.html", {"form": form, "results": results})


def execute_sql_query(sql_input):
    raw_queryset = FitsImage.objects.raw(sql_input)
    return list(fits.PATH for fits in raw_queryset)
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_input)
    #     return cursor.fetchall()


def copy_data(request):
    if request.method == "POST":
        source_paths = request.POST.getlist("source_paths")
        target_path = request.POST.get("target_path")
        print("Source Paths:", source_paths)
        print("Destination Path:", target_path)
        if os.path.exists(target_path):
            status = copy_data_to_target(source_paths, target_path)
        else:
            status = "Target directory doesn't exist."
    return JsonResponse({"status": status})


def copy_data_to_target(source_paths, target_path):
    for source in source_paths:
        try:
            if os.path.exists(source):
                shutil.copy2(source, target_path)
            else:
                return f"Source file {source} does not exist."
        except Exception as e:
            return f"Error copying file: {e}"
    return f"Copied successfully to {target_path}"


def is_valid_sql_query(query):
    query = query.strip()
    if re.search(r"\b(DELETE|DROP|TRUNCATE|CREATE|ALTER|RENAME|INSERT|UPDATE|GRANT|REVOKE)\b", query):
        return False

    # if 'SELECT "*" FROM "Observatory_fitsimage"' in query:
    #     return True

    return True


def add_quotes(query):
    columns = [
        "ID",
        "NAXIS",
        "NAXIS1",
        "NAXIS2",
        "IMAGETYP",
        "FILTER",
        "OBJECT_NAME",
        "SERIES",
        "NOTES",
        "DATE_OBS",
        "MJD_OBS",
        "EXPTIME",
        "CCD_TEMP",
        "XBINNING",
        "YBINNING",
        "XORGSUBF",
        "YORGSUBF",
        "MODE",
        "GAIN",
        "RD_NOISE",
        "OBSERVER",
        "RA",
        "DEC",
        "RA_PNT",
        "DEC_PNT",
        "AZIMUTH",
        "ELEVATIO",
        "AIRMASS",
        "RATRACK",
        "DECTRACK",
        "PHASE",
        "RANGE",
        "PATH",
    ]
    query_words = query.split()

    for i in range(len(query_words)):
        word = query_words[i].upper()
        if word in columns:
            query_words[i] = f'"{word.upper()}"'
        if word[:-1] in columns:
            query_words[i] = f'"{word[:-1].upper()}"'+word[-1]
    updated_query = " ".join(query_words)

    # Add quotes to table name if not already present
    updated_query = re.sub(r"FROM (\w+)", r'FROM "\1"', updated_query, flags=re.IGNORECASE)
    return updated_query

