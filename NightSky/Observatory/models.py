from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FITS_Image(models.Model):
    ID = models.AutoField(primary_key=True)
    NAXIS = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    NAXIS1 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    NAXIS2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    IMAGETYP = models.CharField(max_length=30)
    FILTER = models.CharField(max_length=3, null=True)
    OBJECT_NAME = models.CharField(max_length=100, null=True)
    SERIES = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    NOTES = models.CharField(max_length=1000)
    DATE_OBS = models.CharField(max_length=23)
    MJD_OBS = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100000.00000000)], null=True)
    EXPTIME = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.0)])
    CCD_TEMP = models.FloatField(validators=[MinValueValidator(-50), MaxValueValidator(50)])
    XBINNING = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    YBINNING = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    XORGSUBF = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    YORGSUBF = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)])
    MODE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    GAIN = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100.00)], null=True)
    RD_NOISE = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100.00)], null=True)
    OBSERVER = models.CharField(max_length=30, null=True)
    RA = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.00)], null=True)
    DEC = models.FloatField(validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)], null=True)
    RA_PNT = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.00)], null=True)
    DEC_PNT = models.FloatField(validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)], null=True)
    AZIMUTH = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(360.00)], null=True)
    ELEVATIO = models.FloatField(validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)], null=True)
    AIRMASS = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(1000.000)], null=True)
    RATRACK = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000.00)], null=True)
    DECTRACK = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000.00)], null=True)
    PHASE = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(180.00)], null=True)
    RANGE = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1e27)], null=True)
    PATH = models.CharField(max_length=300)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['DATE_OBS'], name="unique_by_DATE_OBS")
        ]