
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Observatory', '0003_alter_fits_image_airmass_alter_fits_image_azimuth_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FitsImage',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('NAXIS', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('NAXIS1', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)])),
                ('NAXIS2', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)])),
                ('IMAGETYP', models.CharField(blank=True, max_length=30, null=True)),
                ('FILTER', models.CharField(blank=True, max_length=3, null=True)),
                ('OBJECT_NAME', models.CharField(blank=True, max_length=100, null=True)),
                ('SERIES', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('NOTES', models.CharField(blank=True, max_length=1000, null=True)),
                ('DATE_OBS', models.CharField(blank=True, max_length=23, null=True)),
                ('MJD_OBS', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000.0)])),
                ('EXPTIME', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360.0)])),
                ('CCD_TEMP', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-50), django.core.validators.MaxValueValidator(50)])),
                ('XBINNING', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('YBINNING', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('XORGSUBF', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)])),
                ('YORGSUBF', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)])),
                ('MODE', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('GAIN', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100.0)])),
                ('RD_NOISE', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100.0)])),
                ('OBSERVER', models.CharField(blank=True, max_length=30, null=True)),
                ('RA', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360.0)])),
                ('DEC', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)])),
                ('RA_PNT', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360.0)])),
                ('DEC_PNT', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)])),
                ('AZIMUTH', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360.0)])),
                ('ELEVATIO', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)])),
                ('AIRMASS', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000.0)])),
                ('RATRACK', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000.0)])),
                ('DECTRACK', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000.0)])),
                ('PHASE', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(180.0)])),
                ('RANGE', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1e+27)])),
                ('PATH', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='FITS_Image',
        ),
        migrations.AddConstraint(
            model_name='fitsimage',
            constraint=models.UniqueConstraint(fields=('DATE_OBS',), name='unique_by_DATE_OBS'),
        ),
    ]