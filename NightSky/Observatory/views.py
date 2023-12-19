from .forms import DirectoryForm
import django.db.utils
from django.shortcuts import render
from .scripts.parsing import Parsing
from django.db import connection


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    result = ''
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            directory_path = form.cleaned_data['directory_path']
            directory_path = 'C:/Users/anna4/Documents/20230503/' + directory_path[15:]
            p = Parsing(directory_path)
            result = execute_query(str(p))
    else:
        form = DirectoryForm()
    return render(request, 'Observatory/import_fits.html', {'form': form, 'result': result})


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')


# def directory_path_view(request):
#     result = ''
#     if request.method == 'POST':
#         form = DirectoryForm(request.POST)
#         if form.is_valid():
#             directory_path = form.cleaned_data['file_path']
#             p = Parsing(directory_path)
#             result = execute_query(str(p))
#     else:
#         form = DirectoryForm()
#     return render(request, 'Observatory/import_fits.html', {'form': form, 'result': result})


def execute_query(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            return 'DONE'
        except django.db.utils.IntegrityError:
            return 'Already in database'


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')
