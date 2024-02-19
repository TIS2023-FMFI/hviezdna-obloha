from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.forms import MultipleChoiceField

import tkinter as tk
from tkinter import filedialog

import os
import shutil
from typing import List, Union

from .forms import (
    DirectoryForm,
    ExportForm,
    MultipleIntegerIntervalsField,
    MultipleFloatIntervalsField,
    MultipleStringsField,
    DateObsField
)
from .models import FitsImage
from .scripts.csv_writer import CsvWriter
from .scripts.insert import Insert
from .scripts.create_log import Log
from .scripts.first_insert import process_folders_with_fits
from .scripts.generate_sky_map import generate_sky_map
from .scripts.config import Config

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

    path = Config.get_property('Paths', 'fits_archive')

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
    first_insert = FitsImage.objects.count() == 0
    print(first_insert)

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
    if request.method == "POST":

        form = ExportForm(request.POST)
        target_path = request.POST.get("target_directory_path")

        if not target_path:
            return JsonResponse({"error_message": "Directory Error: No target directory selected!"}, status=400)

        # SQL query form processing
        if request.POST.get("is_sql"):
            sql_input = add_quotes(request.POST.get("sql_input"))

            if sql_input:
                try:
                    raw_queryset = execute_sql_query(sql_input)
                    paths = [fits.PATH for fits in raw_queryset]
                    ids = [item.pk for item in raw_queryset]

                    return JsonResponse({
                        "ids": ids,
                        "source_paths": paths,
                        "target_path": target_path
                    })

                except Exception as e:
                    return JsonResponse({"error_message": f"SQL Error: {str(e)}"}, status=500)
            else:
                return JsonResponse({"error_message": "SQL Error: SQL input is empty."}, status=400)

        elif not form.is_valid():
            return JsonResponse({"error_message": f"Form Error: {[value for value in form.errors.values()]}"},
                                status=500)

        # Export form processing
        elif form.is_valid():
            print(form.cleaned_data)
            queryset = FitsImage.objects.get_queryset()

            for field_name, field in form.fields.items():
                field_input = form.cleaned_data.get(field_name)

                if not field_input:
                    continue

                if isinstance(field, (MultipleIntegerIntervalsField, MultipleFloatIntervalsField, DateObsField)):
                    exact_values, intervals = field_input
                    q_objects = Q(**{"%s__in" % field_name: exact_values})

                    for left_endpoint, right_endpoint in intervals:
                        q_objects |= Q(**{"%s__range" % field_name: (left_endpoint, right_endpoint)})

                    queryset = queryset.filter(q_objects)

                if isinstance(field, (MultipleStringsField, MultipleChoiceField)):
                    q_objects = Q(**{"%s__in" % field_name: field_input})
                    queryset = queryset.filter(q_objects)

            paths = queryset.values_list("PATH", flat=True)
            # TODO: remove csv write ???
            csv_writer = CsvWriter(queryset)
            csv_writer.write(target_path)
            ids = [item.pk for item in queryset]
            print(ids)
            print(paths)
            return JsonResponse({"ids": ids, "source_paths": list(paths), "target_path": target_path})

        return redirect("export_fits")

    else:
        form = ExportForm()

    return render(request, "Observatory/export_fits.html", {"form": form})


def execute_sql_query(sql_input):
    return FitsImage.objects.raw(sql_input)
    # with connection.cursor() as cursor:
    #     cursor.execute(sql_input)
    #     return cursor.fetchall()


def copy_data(request):
    if request.method == "POST":
        ids = request.POST.getlist("ids")
        source_paths = request.POST.getlist("source_paths")
        target_path = request.POST.get("target_path")

        # Ensure target path exists
        if not os.path.exists(target_path):
            return JsonResponse({"error_message": "Directory Error: Target directory doesn't exist."}, status=400)

        queryset = FitsImage.objects.filter(pk__in=ids)
        status = copy_data_to_target(source_paths, target_path)

        # Check if copy operation was successful before writing CSV
        if status.startswith("Copied successfully"):
            csv_writer = CsvWriter(queryset)
            csv_writer.write(target_path)
            return JsonResponse({"status": status})

        # If copy_data_to_target() did not return success, return an error response
        return JsonResponse({"error_message": status}, status=400)

    # 405 Method Not Allowed
    return JsonResponse({"error_message": "Invalid request method."}, status=405, headers={"Allow": "POST"})


def copy_data_to_target(source_paths: Union[List[str], List[os.PathLike]], target_path: Union[str, os.PathLike]) -> str:
    for source in source_paths:
        try:
            if os.path.exists(source):
                source_dir, source_filename = os.path.split(source)
                filename_without_ext, file_extension = source_filename.rsplit('.', 1)
                target_filename = f"{filename_without_ext}_{file_extension}.fit"
                full_target_path = os.path.join(target_path, target_filename)

                shutil.copy2(str(source), str(full_target_path))
            else:
                return f"Source file {source} does not exist."
        except Exception as e:
            return f"Error copying file: {e}"
    return f"Copied successfully to {target_path}"


def is_valid_sql_query(query):
    disallowed_keywords = r"\b(DELETE|DROP|TRUNCATE|CREATE|ALTER|RENAME|INSERT|UPDATE|GRANT|REVOKE)\b"
    return not re.search(disallowed_keywords, query.strip(), re.IGNORECASE)


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
        if word in columns:  # if the column name does not contain quotes and contains a space before the operator
            query_words[i] = f'"{word}"'
        elif word[1:-1] in columns:  # if the column name contains quotes and a space before the operator
            query_words[i] = f'"{word[1:-1]}"'
        elif len(word) > 1 and any(op in word for op in [">=", "<=", "<", ">", "=", ","]):
            operator = get_comparison_operator(word)
            position = word.find(operator)
            if word[:position] in columns:  # if the column name does not contain quotes and a space before the operator
                query_words[i] = f'"{word[:position]}"' + word[position:]
            if word[
               1:position - 1] in columns:  # if the column name contains quotes and does not contain a space before the operator
                query_words[i] = f'"{word[1:position - 1]}"' + word[position:]

    updated_query = " ".join(query_words)

    # Add quotes to table name if not already present
    updated_query = re.sub(r"FROM (\w+)", r'FROM "\1"', updated_query, flags=re.IGNORECASE)
    return updated_query


def get_comparison_operator(word):
    comparison_operators = [">=", "<=", "<", ">", "=", ","]
    for op in comparison_operators:
        if op in word:
            return op
    return None