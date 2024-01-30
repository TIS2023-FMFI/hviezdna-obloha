from ..models import FitsImage
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt


def generate_sky_map():
    # Fetch data from the database
    fits_images = FitsImage.objects.all()

    sky_coverage_data = [
        {"ra": image.RA, "dec": image.DEC} for image in fits_images if image.RA is not None and image.DEC is not None
    ]

    # Convert RA and DEC to radians for Aitoff projection
    ra = [data["ra"] for data in sky_coverage_data]
    dec = [data["dec"] for data in sky_coverage_data]
    c = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, frame="icrs")
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
    plt.savefig(r"static\sky_coverage_map.png", bbox_inches="tight")
    plt.close()
