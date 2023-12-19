from django.urls import path
from .views import home, import_fits, export_fits

urlpatterns = [
    path('', home, name='home'),
    path('import_fits/', import_fits, name='import_fits'),
    path('export_fits/', export_fits, name='export_fits'),
]
