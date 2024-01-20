import os

from astropy.io import fits


class Parsing:
    def __init__(self, path):
        self.path = path
        self.query = None
        self.PARAMETERS = [
            'NAXIS', 'NAXIS1', 'NAXIS2', 'IMAGETYP', 'FILTER', 'OBJECT', 'SERIES', 'NOTES', 'DATE-OBS',
            'MJD-OBS', 'EXPTIME', 'CCD-TEMP', 'XBINNING', 'YBINNING', 'XORGSUBF', 'YORGSUBF', 'MODE',
            'GAIN', 'RD_NOISE', 'OBSERVER', 'RA', 'DEC', 'RA_PNT', 'DEC_PNT', 'AZIMUTH', 'ELEVATIO',
            'AIRMASS', 'RATRACK', 'DECTRACK', 'PHASE', 'RANGE', 'PATH'
        ]

        self.start_query()
        self.add_all_images(path)

    def add_all_images(self, path):
        for image in os.listdir(path):
            self.query += str(Values(path + '/' + image, self.PARAMETERS))
            self.query += ',\n'

        self.query = self.query[:-2]
        self.query += ';'

    def start_query(self):
        self.query = 'INSERT INTO \"Observatory_fits_image\" ('
        param_insert = self.PARAMETERS

        for param in param_insert:
            if '-' in param:
                param = param.replace('-', '_')
            if param == 'OBJECT':
                param = 'OBJECT_NAME'
            self.query += '\"' + param + '\", '

        self.query = self.query[:-2] + ') \nVALUES '

    def __str__(self):
        return self.query


class Values:
    def __init__(self, image_path, parameters):
        self.parameters = parameters

        my_fits = fits.open(image_path)
        self.header = my_fits[0].header
        my_fits.close()

        self.image_path = image_path
        self.VALUES = '('

        self.insert_image()

    def __str__(self):
        return self.VALUES

    def insert_image(self):
        for param in self.parameters[:-1]:
            if param == 'OBJECT':
                self.values_add_value(self.split_object()[0])
            elif param == 'SERIES' and '_' in self.header['OBJECT']:
                self.values_add_value(self.split_object()[1])
            elif param == 'RA' or param == 'DEC':
                self.try_add(param + '_PNT')
            else:
                self.try_add(param)

            self.values_add_syntax(', ')

        self.values_add_value(self.image_path)
        self.values_add_syntax(')')

    def try_add(self, param):
        try:
            value = str(self.header[param])
            if param == 'NOTES' and value == '':
                self.values_add_value(' ')
            else:
                self.values_add_value(value)

        except KeyError:
            self.values_add_syntax('NULL')

    def split_object(self):
        return str(self.header['OBJECT']).split('_')

    def values_add_value(self, value):
        if value == '':
            self.VALUES += 'NULL'
        else:
            self.VALUES += '\'' + value + '\''

    def values_add_syntax(self, syntax):
        self.VALUES += syntax
