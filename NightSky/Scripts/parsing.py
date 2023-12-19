from astropy.io import fits
import os


class Parsing:
    def __init__(self, path):
        self.path = path
        self.PARAMETERS = ['NAXIS', 'NAXIS1', 'NAXIS2', 'IMAGETYP', 'FILTER', 'OBJECT', 'SERIES', 'NOTES', 'DATE-OBS',
                           'MJD-OBS', 'EXPTIME', 'CCD-TEMP', 'XBINNING', 'YBINNING', 'XORGSUBF', 'YORGSUBF', 'MODE',
                           'GAIN', 'RD_NOISE', 'OBSERVER', 'RA', 'DEC', 'RA_PNT', 'DEC_PNT', 'AZIMUTH', 'ELEVATIO',
                           'AIRMASS', 'RATRACK', 'DECTRACK', 'PHASE', 'RANGE', 'PATH']
        self.start_query()
        self.add_all_images(path)

    def add_all_images(self, path):
        for image in os.listdir(path):
            self.QUERY += str(Values(path + image, self.PARAMETERS))
            self.QUERY += ',\n'
        self.QUERY = self.QUERY[:-2]
        self.QUERY += ';'

    def start_query(self):
        self.QUERY = 'INSERT INTO fits_images ('
        for param in self.PARAMETERS:
            self.QUERY += param + ', '
        self.QUERY = self.QUERY[:-2] + ') \nVALUES '

    def __str__(self):
        return self.QUERY


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
            elif param == 'SERIES':
                self.values_add_value(self.split_object()[1])
            else:
                self.try_add(param)
            self.values_add_syntax(', ')
        self.values_add_value(self.image_path)
        self.values_add_syntax(')')

    def try_add(self, param):
        try:
            self.values_add_value(str(self.header[param]))
        except KeyError:
            self.values_add_syntax('NULL')

    def split_object(self):
        return str(self.header['OBJECT']).split('_')

    def values_add_value(self, value):
        self.VALUES += '\"' + value + '\"'

    def values_add_syntax(self, syntax):
        self.VALUES += syntax