from django.shortcuts import render
from .forms import DirectoryForm


def home(request):
    return render(request, 'Observatory/home.html')


def import_fits(request):
    return render(request, 'Observatory/import_fits.html')


def export_fits(request):
    return render(request, 'Observatory/export_fits.html')


def directory_path_view(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            file_path = form.cleaned_data['file_path']
            # Process the path ...
    else:
        form = DirectoryForm()

    return render(request, 'Observatory/import_fits.html', {'form': form})
