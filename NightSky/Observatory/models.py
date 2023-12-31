from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FITS_Image(models.Model):
    ID = models.AutoField(primary_key=True)
    NAXIS = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    NAXIS1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    NAXIS2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    IMAGETYP = models.CharField(max_length=10)
    FILTER = models.CharField(max_length=3)
    OBJECT_NAME = models.CharField(max_length=100)
    SERIES = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    NOTES = models.CharField(max_length=1000)
    DATE_OBS = models.CharField(max_length=23)
    MJD_OBS = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100000.00000000)])
    EXPTIME = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.0)])
    CCD_TEMP = models.FloatField(validators=[MinValueValidator(-50), MaxValueValidator(50)])
    XBINNING = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    YBINNING = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    XORGSUBF = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    YORGSUBF = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    MODE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    GAIN = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100.00)])
    RD_NOISE = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100.00)])
    OBSERVER = models.CharField(max_length=30)
    RA = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.00)])
    DEC = models.FloatField(validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)])
    RA_PNT = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.00)])
    DEC_PNT = models.FloatField(validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)])
    AZIMUTH = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.00)])
    ELEVATIO = models.FloatField(validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)])
    AIRMASS = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(1000.000)])
    RATRACK = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000.00)])
    DECTRACK = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000.00)])
    PHASE = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(180.00)])
    RANGE = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1e27)])
    PATH = models.CharField(max_length=300)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['DATE_OBS'], name="unique_by_DATE_OBS")
        ]