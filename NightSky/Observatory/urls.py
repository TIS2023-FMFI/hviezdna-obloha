from django.urls import path
from .views import home, import_fits, export_fits, open_file_explorer

urlpatterns = [
    path('', home, name='home'),
    path('import_fits/', import_fits, name='import_fits'),
    path('export_fits/', export_fits, name='export_fits'),
    path('open-file-explorer/', open_file_explorer, name='open_file_explorer')
]
