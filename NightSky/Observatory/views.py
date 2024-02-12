import json
import django.db.utils
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from django.contrib import messages

from .forms import DirectoryForm, ExportForm
from .models import FitsImage
from .scripts.first_insert import process_folders_with_fits
from .scripts.insert import Insert
from .scripts.create_log import Log
from .scripts.generate_sky_map import generate_sky_map

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from django.contrib import messages
from datetime import datetime, timedelta
import shutil

from datetime import datetime, timedelta
import re


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
    path = r"D:\TIS\20230503"

    # Get the last added directory path in the archive
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    directories.sort(key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
    last_added_directory_path = os.path.join(path, directories[0]) if directories else None
    inserted_rows = 0

    if request.method == "POST":
        if "import_last_night" in request.POST and last_added_directory_path:
            directory_path = last_added_directory_path
            inserted_rows = process_and_log_directory(directory_path, request)
            if inserted_rows > 0:
                messages.success(request, f"Import successful")
            else:
                messages.error(request, f"Import failed.")
            request.session["form_submitted"] = "import_last_night"

        elif "import_directory" in request.POST:
            if form.is_valid():
                directory_path = form.cleaned_data["directory_path"]
                inserted_rows = process_and_log_directory(directory_path, request)
                if inserted_rows > 0:
                    messages.success(request, f"Import successful")
                else:
                    messages.error(request, f"Import failed.")
            else:
                messages.error(request, "Incorrect input: Please ensure the directory path is correct.")
            request.session["form_submitted"] = "import_directory"

    return render(
        request, "Observatory/import_fits.html", {"form": form, "last_added_directory_path": last_added_directory_path}
    )


def process_and_log_directory(directory_path, request):
    first_insert = False
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


def export_fits(request):
    results = None
    if request.method == "POST":
        form = ExportForm(request.POST)
        # SQL query form processing
        if "sql_export" in request.POST:
            target_path = request.POST.get("target_directory_path")
            if target_path == "":
                return JsonResponse({"error_message": "No target directory selected!"})
            sql_input = add_quotes(request.POST.get("sql_input"))
            try:
                if is_valid_sql_query(sql_input):
                    results = execute_sql_query(sql_input)
                    print([r[0] for r in results])
                    return JsonResponse({"source_paths": [path[0] for path in results], "target_path": target_path})
                else:
                    return JsonResponse({"error_message": "Wrong SQL query"})
            except Exception as e:
                return JsonResponse({"error_message": f"Error executing the SQL query: {e}"})
        # end of SQL query form processing

        elif form.is_valid():
            return render(request, "Observatory/export_fits.html", {"form": form, "results": results})
    else:
        form = ExportForm()
    return render(request, "Observatory/export_fits.html", {"form": form, "results": results})


def execute_sql_query(sql_input):
    with connection.cursor() as cursor:
        cursor.execute(sql_input)
        return cursor.fetchall()


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


def is_valid_sql_query(query):
    query = query.strip()
    if re.search(r"\b(DELETE|DROP|TRUNCATE)\b", query):
        return False

    if 'SELECT "PATH" FROM "Observatory_fitsimage"' in query:
        return True

    return False


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
    print(query_words)

    for i in range(len(query_words)):
        word = query_words[i].upper()
        if word in columns:
            query_words[i] = f'"{word.upper()}"'
    updated_query = " ".join(query_words)

    # Add quotes to table name if not already present
    updated_query = re.sub(r"FROM (\w+)", r'FROM "\1"', updated_query, flags=re.IGNORECASE)

    return updated_query
