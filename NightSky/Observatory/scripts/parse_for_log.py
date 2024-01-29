from astropy.io import fits
from astropy.time import Time


class ParseForLog:
    def __init__(self, image_path, num):

        self.series = ''
        self.obj = ''
        self.filter = ''

        try:
            my_fits = fits.open(image_path, ignore_missing_simple=True)
            self.header = my_fits[0].header
            my_fits.close()
        except OSError:
            self.data = ''
            self.header = None
            return

        self.NUM_OF_EMPTY_COLUMNS = 4
        self.data = [num]

    def get_data(self):
        return self.data

    def add_data(self):

        self.data.append('ASTRO')

        self.add_object_series()

        date_obs = Time(self.get_value_of('DATE-OBS'), format='fits')
        self.data.append(date_obs.datetime.strftime('%H:%M:%S'))

        self.filter = self.get_value_of('FILTER')
        self.data.append(self.filter)

        self.data.append(str(self.get_value_of('NAXIS1')) + 'x' + str(self.get_value_of('NAXIS2')))

        self.data.append(self.get_value_of('EXPTIME'))

        self.data.append('0')

    def add_object_series(self):
        value = self.get_value_of('OBJECT')
        values = value.split('_')
        self.obj = values[0]
        self.data.append(self.obj)
        try:
            self.series = values[1]
            self.data.append(self.series)
        except IndexError:
            self.data.append('')

    def get_value_of(self, keyword):
        try:
            return self.header[keyword]
        except KeyError:
            return ''

    def get_data_for_n(self):
        return self.obj, self.series, self.filter

    def has_header(self):
        return self.header is not None
