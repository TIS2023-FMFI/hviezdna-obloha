from django.contrib import admin
from .models import FitsImage


class FitsImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(FitsImage, FitsImageAdmin)
