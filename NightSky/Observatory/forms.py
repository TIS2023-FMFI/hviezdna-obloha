from django import forms

from .models import FitsImage


class DirectoryForm(forms.Form):
    directory_path = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Directory path",
                "id": "directory_path",
                "name": "directory_path",
                "type": "text",
            }
        ),
        required=True,
    )


# TODO: zlepsit medzery v inpute
class DateObsField(forms.CharField):
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

                # if not is_integer(left_endpoint) or not is_integer(right_endpoint):
                #     raise forms.ValidationError("Invalid format.")

                if left_endpoint > right_endpoint:
                    raise forms.ValidationError(
                        "First endpoint of an interval must not be greater than the second one.")

                # TODO: POZOR TU JE ZRADA DO BUDUCNA
                integer_intervals.append((left_endpoint, right_endpoint))
                raw_left_endpoint = ""

            elif is_integer(raw_value):
                clean_integers.append(int(raw_value))

        if raw_left_endpoint:
            raise forms.ValidationError("Invalid format.")

        return clean_integers, integer_intervals

    def validate(self, value):
        super().validate(value)


class MultipleStringsField(forms.CharField):
    def to_python(self, value):
        value = value.replace(" ", "")

        if not value:
            return None

        return value.split(",")

    def validate(self, value):
        super().validate(value)


def is_integer(value):
    try:
        int(value)
    except ValueError:
        raise forms.ValidationError("Invalid format.")

    return True


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
        super().validate(value)


def is_float(value):
    try:
        float(value)
    except ValueError:
        raise forms.ValidationError("Invalid format.")

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
        super().validate(value)


class ExportForm(forms.Form):
    primary_fields = ['OBJECT_NAME', 'SERIES', 'EXPTIME', 'FILTER', 'DATE_OBS', 'IMAGETYP', 'CCD_TEMP', 'RA', 'DEC']

    OBJECT_NAME = MultipleStringsField(widget=forms.TextInput(attrs={"placeholder": "String"}), required=False)
    SERIES = MultipleStringsField(widget=forms.TextInput(attrs={"placeholder": "String"}), required=False)
    EXPTIME = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    FILTER = MultipleStringsField(widget=forms.TextInput(attrs={"placeholder": "String"}), required=False)
    DATE_OBS = DateObsField(widget=forms.TextInput(attrs={"placeholder": "String"}), required=False)
    IMAGETYP = MultipleStringsField(widget=forms.TextInput(attrs={"placeholder": "String"}), required=False)
    CCD_TEMP = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    RA = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    DEC = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)

    NAXIS = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    NAXIS1 = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    NAXIS2 = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    XBINNING = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    YBINNING = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    XORGSUBF = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    YORGSUBF = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)
    MODE = MultipleIntegerIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Integer"}), required=False)

    MJD_OBS = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    GAIN = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    RD_NOISE = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    RA_PNT = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    DEC_PNT = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    AZIMUTH = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    ELEVATIO = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    AIRMASS = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    RATRACK = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    DECTRACK = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    PHASE = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)
    RANGE = MultipleFloatIntervalsField(widget=forms.TextInput(attrs={"placeholder": "Float"}), required=False)

    OBSERVER = MultipleStringsField(widget=forms.TextInput(attrs={"placeholder": "String"}), required=False)

    #
    # OBJECT_NAME = forms.MultipleChoiceField(
    #     choices=object_name_choices, widget=forms.CheckboxSelectMultiple, required=False
    # )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["OBJECT_NAME"].choices = [
    #         (image.OBJECT_NAME, image.OBJECT_NAME)
    #         for image in FitsImage.objects.all().distinct("OBJECT_NAME").order_by("OBJECT_NAME")
    #     ]