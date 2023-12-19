from django.shortcuts import render
from .forms import ImportFITSForm


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    return render(request, 'Observatory/import_fits.html')


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')
