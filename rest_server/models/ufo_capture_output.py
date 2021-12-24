from django.db import models

from rest_server.models import Report
from rest_server.utils import model2str


class UfoCaptureOutputEntry(models.Model):

    snapshot_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  'One frame at the trigger will be saved as a still image. '
                  'Exclusive with PeakHold setting.'
    )
    peak_hold_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  'Automatic composite still image which contains the peak brightness of each pixel'
                  ' during the detection will be saved as a still image.'
    )
    thumbnail_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  'Small size jpeg image for realtime transfer.'
    )

    # ???
    internal_thumbnail_pathname = models.CharField(
        max_length=260,
        help_text='Pathname of the thumbnail stored on the server.'
    )

    map_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  '*M.bmp which contains layered information of the event.'
    )
    clip_filename = models.CharField(
        max_length=260,
        help_text='Filename of a clip file on the remote station.'
    )
    xml_filename = models.CharField(
        max_length=260,
        help_text='Filename of a xml file on the remote station. '
    )
    type = models.CharField(
        choices=[
            ('r', 'Recording'),
            ('t', 'Trigger')
        ],
        help_text='Type of the UFOCapture entry'

    )

    filename_datetime = models.DateTimeField(
        help_text='Datetime value derived from from UFOCapture file.',
        null=True
    )

    version = models.CharField(
        max_length=20,
        help_text='Value of attribute "version" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    xml_datetime = models.DateTimeField(
        help_text='Datetime value from from UFOCapture XML file.',
        null=True
    )
    trig = models.IntegerField(
        help_text='Value of attribute "trig" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    frames = models.IntegerField(
        help_text='Value of attribute "frames" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    lng = models.FloatField(
        help_text='Value of attribute "lng" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    lat = models.FloatField(
        help_text='Value of attribute "lat" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    alt = models.FloatField(
        help_text='Value of attribute "alt" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    tz = models.CharField(
        max_length=20,
        help_text='Value of attribute "tz" of ufocapture_record inside UFOCapture XML file.'
    )
    u2 = models.IntegerField(
        help_text='Value of attribute "u2" of ufocapture_record inside UFOCapture XML file.'
    )
    cx = models.IntegerField(
        help_text='Value of attribute "cx" of ufocapture_record inside UFOCapture XML file.'
    )
    cy = models.IntegerField(
        help_text='Value of attribute "cy" of ufocapture_record inside UFOCapture XML file.'
    )
    fps = models.FloatField(
        help_text='Value of attribute "fps" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    head = models.IntegerField(
        help_text='Value of attribute "head" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    tail = models.IntegerField(
        help_text='Value of attribute "tail" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    diff = models.IntegerField(
        help_text='Value of attribute "diff" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    sipos = models.IntegerField(
        help_text='Value of attribute "sipos" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    sisize = models.IntegerField(
        help_text='Value of attribute "sisize" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    dlev = models.IntegerField(
        help_text='Value of attribute "dlev" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    dsize = models.IntegerField(
        help_text='Value of attribute "dsize" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    countrycode = models.CharField(
        max_length=2,
        help_text='Value of attribute "countrycode" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    lid = models.CharField(
        max_length=16,
        help_text='Value of attribute "lid" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    observer = models.CharField(
        max_length=32,
        help_text='Value of attribute "observer" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    sid = models.CharField(
        max_length=16,
        help_text='Value of attribute "sid" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    cam = models.CharField(
        max_length=32,
        help_text='Value of attribute "cam" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    lens = models.CharField(
        max_length=32,
        help_text='Value of attribute "lens" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    cap = models.CharField(
        max_length=32,
        help_text='Value of attribute "cap" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    comment = models.CharField(
        max_length=64,
        help_text='Value of attribute "comment" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    interlace = models.IntegerField(
        help_text='Value of attribute "interlace" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    bbf = models.IntegerField(
        help_text='Value of attribute "bbf" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    dropframe = models.IntegerField(
        help_text='Value of attribute "dropframe" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )
    fourcc = models.IntegerField(
        help_text='Value of attribute "fourcc" of ufocapture_record inside UFOCapture XML file.',
        null=True
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        model_name = self.__class__.__name__
        field_value_strs = []

        for field in ['clip_filename', 'type']:
            v = getattr(self, field.name)
            v_str = f'"{v}"' if isinstance(v, str) else v
            field_value_strs.append(f'{field.name}: {v_str}')

        return f'{model_name} ({", ".join(field_value_strs)})'