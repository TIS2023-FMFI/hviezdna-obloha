from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FitsImage(models.Model):
    ID = models.AutoField(primary_key=True)
    NAXIS = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)
    NAXIS1 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        blank=True,
        null=True,
    )
    NAXIS2 = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        blank=True,
        null=True,
    )
    IMAGETYP = models.CharField(max_length=30, blank=True, null=True)
    FILTER = models.CharField(max_length=3, blank=True, null=True)
    OBJECT_NAME = models.CharField(max_length=100, blank=True, null=True)
    SERIES = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    NOTES = models.CharField(max_length=1000, blank=True, null=True)
    DATE_OBS = models.CharField(max_length=23, blank=True, null=True)
    MJD_OBS = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100000.00000000)],
        blank=True,
        null=True,
    )
    EXPTIME = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(360.0)],
        blank=True,
        null=True,
    )
    CCD_TEMP = models.FloatField(
        validators=[MinValueValidator(-50), MaxValueValidator(50)],
        blank=True,
        null=True,
    )
    XBINNING = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    YBINNING = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    XORGSUBF = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        blank=True,
        null=True,
    )
    YORGSUBF = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        blank=True,
        null=True,
    )
    MODE = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)
    GAIN = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100.00)],
        blank=True,
        null=True,
    )
    RD_NOISE = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100.00)],
        blank=True,
        null=True,
    )
    OBSERVER = models.CharField(max_length=30, blank=True, null=True)
    RA = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(360.00)],
        blank=True,
        null=True,
    )
    DEC = models.FloatField(
        validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)],
        blank=True,
        null=True,
    )
    RA_PNT = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(360.00)],
        blank=True,
        null=True,
    )
    DEC_PNT = models.FloatField(
        validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)],
        blank=True,
        null=True,
    )
    AZIMUTH = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(360.00)],
        blank=True,
        null=True,
    )
    ELEVATIO = models.FloatField(
        validators=[MinValueValidator(-90.00), MaxValueValidator(90.00)],
        blank=True,
        null=True,
    )
    AIRMASS = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(1000.000)],
        blank=True,
        null=True,
    )
    RATRACK = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000.00)],
        blank=True,
        null=True,
    )
    DECTRACK = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000.00)],
        blank=True,
        null=True,
    )
    PHASE = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(180.00)],
        blank=True,
        null=True,
    )
    RANGE = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1e27)],
        blank=True,
        null=True,
    )
    PATH = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["DATE_OBS"], name="unique_by_DATE_OBS")]
