from django.core.management.base import BaseCommand
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord
from ...models import FITS_Image


class Command(BaseCommand):
    help = 'Generates a sky coverage map and saves it to the static folder'

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        fits_images = FITS_Image.objects.all()

        sky_coverage_data = [{'ra': image.RA, 'dec': image.DEC} for image in fits_images]

        # Convert RA and DEC to radians for Aitoff projection
        ra = [data['ra'] - 180 for data in sky_coverage_data]
        dec = [data['dec'] for data in sky_coverage_data]
        c = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame='icrs')
        ra_rad = c.ra.wrap_at(180 * u.deg).radian
        dec_rad = c.dec.radian

        # Create Aitoff projection plot
        plt.figure(figsize=(16, 8))

        plt.subplot(111, projection="aitoff")
        plt.grid(True)
        plt.scatter(ra_rad, dec_rad, s=1)

        plt.title("Sky Coverage Map", pad=30)
        plt.xlabel("Right Ascension", labelpad=20)
        plt.ylabel("Declination", labelpad=20)

        # Save the plot as an image in the static folder
        plt.savefig(r'static\sky_coverage_map.png', bbox_inches='tight')

        self.stdout.write(self.style.SUCCESS('Successfully generated sky map'))
