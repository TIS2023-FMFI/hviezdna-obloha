from django.urls import path
from .views import home, import_fits, export_fits  # , directory_path_view

urlpatterns = [
    path("", home, name="home"),
    path("import_fits/", import_fits, name="import_fits"),
    path("export_fits/", export_fits, name="export_fits"),
    # path('import_fits/', directory_path_view, name='import_fits')
]
