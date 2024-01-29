from astropy.io import fits
from django.db import IntegrityError
import os
from ..models import FITS_Image


class Insert:

    def __init__(self, path):
        self.path = path
        self.parameters = ['NAXIS', 'NAXIS1', 'NAXIS2', 'IMAGETYP', 'FILTER', 'OBJECT', 'NOTES', 'DATE-OBS',
                           'MJD-OBS', 'EXPTIME', 'CCD-TEMP', 'XBINNING', 'YBINNING', 'XORGSUBF', 'YORGSUBF', 'MODE',
                           'GAIN', 'RD_NOISE', 'OBSERVER', 'RA', 'DEC', 'RA_PNT', 'DEC_PNT', 'AZIMUTH', 'ELEVATIO',
                           'AIRMASS', 'RATRACK', 'DECTRACK', 'PHASE', 'RANGE']
        self.query_dicts = []
        self.parse()
        self.insert()

    def insert(self):
        instances = [FITS_Image(**v) for v in self.query_dicts]
        try:
            FITS_Image.objects.bulk_create(instances, ignore_conflicts=True)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")

    def parse(self):
        for image in os.listdir(self.path):
            try:
                p = Parsing(self.path + '/' + image, self.parameters)
                self.query_dicts.append(p.get_values_dict())
            except OSError:
                pass


def time_to_decimal(time_string):
    if time_string == '':
        return ''
    hours, minutes, seconds = map(float, time_string.split(':'))
    decimal_hours = hours + (minutes / 60) + (seconds / 3600)
    return decimal_hours


class Parsing:

    def __init__(self, image_path, param):
        self.path = image_path

        try:
            my_fits = fits.open(self.path, ignore_missing_simple=True)
            self.header = my_fits[0].header
            my_fits.close()
        except OSError:
            raise OSError

        self.parameters = param
        self.values = {'PATH': self.path}

        self.set_values()

        self.repair_object()

    def repair_object(self):
        try:
            object_series = self.values['OBJECT']
        except KeyError:
            return

        if '_' in object_series:
            object_series = object_series.split('_')
            obj = object_series[0]
            self.values['SERIES'] = object_series[1]
        else:
            obj = self.values['OBJECT']

        self.values.pop('OBJECT')
        self.values['OBJECT_NAME'] = obj

    def set_values(self):
        for param in self.parameters[:-1]:
            value = self.get_value(param)

            if param in ['DATE-OBS', 'MJD-OBS', 'CCD-TEMP']:
                param = param.replace('-', '_')

            elif param in ['RA', 'DEC']:
                value = time_to_decimal(value)

            if value != '':
                self.values[param] = value

    def get_value(self, param):
        try:
            return str(self.header[param])
        except KeyError:
            return ''

    def get_values_dict(self):
        return self.values
