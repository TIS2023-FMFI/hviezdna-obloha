from django import forms
from .models import FitsImage


class DirectoryForm(forms.Form):
    directory_path = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Directory path", "id": "directory_path", "name": "directory_path", "type": "text"}
        ),
        required=True,
    )


class MultipleStringsField(forms.CharField):
    def to_python(self, value):
        value = value.replace(" ", "")

        if not value:
            return None

        return value.split(",")

    def validate(self, value):
        # super().validate(value)
        # if value is None:
        #     return
        return


class MultipleIntegerIntervalsField(forms.CharField):
    def to_python(self, value):
        value = value.replace(" ", "")

        if not value:
            return None

        clean_integers = []
        integer_intervals = []
        raw_left_endpoint = ""
        input_values = value.split(",")

        for raw_value in input_values:
            if "[" in raw_value and raw_left_endpoint:
                raise forms.ValidationError("Invalid format.")

            elif "[" in raw_value:
                raw_left_endpoint = raw_value

            elif "]" in raw_value and not raw_left_endpoint:
                raise forms.ValidationError("Invalid format.")

            elif "]" in raw_value:
                left_endpoint = raw_left_endpoint[1:]
                right_endpoint = raw_value[:-1]

                if not is_integer(left_endpoint) or not is_integer(right_endpoint):
                    raise forms.ValidationError("Invalid format.")

                left_endpoint = int(left_endpoint)
                right_endpoint = int(right_endpoint)

                if left_endpoint > right_endpoint:
                    raise forms.ValidationError("First endpoint of an interval must be smaller than the second one.")

                # TODO: POZOR TU JE ZRADA DO BUDUCNA
                integer_intervals.append((left_endpoint, right_endpoint))
                raw_left_endpoint = ""

            elif is_integer(raw_value):
                clean_integers.append(int(raw_value))

        if raw_left_endpoint:
            raise forms.ValidationError("Invalid format.")

        return clean_integers, integer_intervals

    def validate(self, value):
        # super().validate(value)
        # if value is None:
        #     return
        return


def is_integer(value):
    try:
        int(value)
    except ValueError:
        raise forms.ValidationError("Invalid woof format.")

    return True


def is_float(value):
    try:
        float(value)
    except ValueError:
        raise forms.ValidationError("Invalid woof format.")

    return True


class MultipleFloatIntervalsField(forms.CharField):
    def to_python(self, value):
        value = value.replace(" ", "")

        if not value:
            return None

        clean_floats = []
        float_intervals = []
        raw_left_endpoint = ""
        input_values = value.split(",")

        for raw_value in input_values:
            if "[" in raw_value and raw_left_endpoint:
                raise forms.ValidationError("Invalid format.")

            elif "[" in raw_value:
                raw_left_endpoint = raw_value

            elif "]" in raw_value and not raw_left_endpoint:
                raise forms.ValidationError("Invalid format.")

            elif "]" in raw_value:
                left_endpoint = raw_left_endpoint[1:]
                right_endpoint = raw_value[:-1]

                if not is_float(left_endpoint) or not is_float(right_endpoint):
                    raise forms.ValidationError("Invalid format.")

                left_endpoint = float(left_endpoint)
                right_endpoint = float(right_endpoint)

                if left_endpoint > right_endpoint:
                    raise forms.ValidationError("First endpoint of an interval must be smaller than the second one.")

                # TODO: POZOR TU JE ZRADA DO BUDUCNA
                float_intervals.append((left_endpoint, right_endpoint))
                raw_left_endpoint = ""

            elif is_float(raw_value):
                clean_floats.append(float(raw_value))

        if raw_left_endpoint:
            raise forms.ValidationError("Invalid format.")

        return clean_floats, float_intervals

    def validate(self, value):
        # super().validate(value)
        # if value is None:
        #     return
        return


class ExportForm(forms.Form):
    NAXIS = MultipleIntegerIntervalsField()
    NAXIS1 = MultipleIntegerIntervalsField()
    NAXIS2 = MultipleIntegerIntervalsField()

    IMAGETYP = MultipleStringsField()
    FILTER = MultipleStringsField()
    # OBJECT_NAME = MultipleStringsField()
    SERIES = MultipleStringsField()
    DATE_OBS = MultipleStringsField()

    MJD_OBS = MultipleFloatIntervalsField()
    EXPTIME = MultipleFloatIntervalsField()
    CCD_TEMP = MultipleFloatIntervalsField()

    XBINNING = MultipleIntegerIntervalsField()
    YBINNING = MultipleIntegerIntervalsField()
    XORGSUBF = MultipleIntegerIntervalsField()
    YORGSUBF = MultipleIntegerIntervalsField()
    MODE = MultipleIntegerIntervalsField()

    GAIN = MultipleFloatIntervalsField()
    RD_NOISE = MultipleFloatIntervalsField()

    OBSERVER = MultipleStringsField()

    RA = MultipleFloatIntervalsField()
    DEC = MultipleFloatIntervalsField()
    RA_PNT = MultipleFloatIntervalsField()
    DEC_PNT = MultipleFloatIntervalsField()
    AZIMUTH = MultipleFloatIntervalsField()
    ELEVATIO = MultipleFloatIntervalsField()
    AIRMASS = MultipleFloatIntervalsField()
    RATRACK = MultipleFloatIntervalsField()
    DECTRACK = MultipleFloatIntervalsField()
    PHASE = MultipleFloatIntervalsField()
    RANGE = MultipleFloatIntervalsField()

    object_name_choices = [
        (image.ID, image.OBJECT_NAME)
        for image in FitsImage.objects.all().distinct("OBJECT_NAME").order_by("OBJECT_NAME")
    ]

    OBJECT_NAME = forms.MultipleChoiceField(choices=object_name_choices, widget=forms.CheckboxSelectMultiple)

    # class Meta:
    #     model = FitsImage
    #     exclude = ["PATH"]
