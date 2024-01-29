from .forms import DirectoryForm
import django.db.utils
from django.shortcuts import render
from .scripts.first_insert import process_folders_with_fits
from .scripts.insert import Insert
from .scripts.create_log import Log
from django.db import connection


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    result = ''
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory_path = form.cleaned_data['directory_path']
            directory_path = 'D:/' + directory_path[15:] #change to your path to fits images instead of 'D:/'

            first_insert = False
            if first_insert:
                process_folders_with_fits(directory_path)
            else:
                # daily insert with generating log
                insert = Insert(directory_path)
                del insert
                log = Log(directory_path)
                log.generate_log()

    else:
        form = DirectoryForm()
    return render(request, 'Observatory/import_fits.html', {'form': form, 'result': result})


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')

