import os.path

from django.apps import apps
from django.db import models

from rest_server.models.station import Station
from rest_server.models.report import Report


def get_base_preview_image_dir_path(station_name):
    return os.path.join(
        apps.get_app_config('rest_server').REPORT_BASE_DATA_DIR,
        str(station_name),
    )


def get_preview_image_dir_path(
        station_name,
        report_start_utc,
        report_hash,
        filename,
):
    return os.path.join(
        get_base_preview_image_dir_path(station_name),
        '{:%Y%m%d-%H%M%S}--{}'.format(
            report_start_utc,
            report_hash
        ),
        filename
    )


def preview_image_dir_path(instance, filename):
    # If you are using the default FileSystemStorage,
    # the string value will be appended to your MEDIA_ROOT path
    # to form the location on the local filesystem where uploaded files will be stored.
    return get_preview_image_dir_path(
        instance.station.name,
        instance.report.start_utc,
        instance.report.hash,
        filename,
    )



class UfoCaptureOutputEntry(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['report', 'clip_filename'], name='unique_pair_report_clip'),
            models.UniqueConstraint(fields=['station', 'clip_filename'], name='unique_pair_station_clip')
        ]
        verbose_name_plural = "ufo capture output entries"

    snapshot_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  'One frame at the trigger will be saved as a still image. '
                  'Exclusive with PeakHold setting.',
        blank=True, null=True
    )
    peak_hold_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  'Automatic composite still image which contains the peak brightness of each pixel'
                  ' during the detection will be saved as a still image.',
        blank=True, null=True
    )
    thumbnail_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  'Small size jpeg image for realtime transfer.',
        blank=True, null=True
    )

    # ???
    # internal_thumbnail_pathname = models.CharField(
    #     max_length=260,
    #     help_text='Pathname of the thumbnail stored on the server.',
    #     blank=True, null=True
    # )

    det_level_preview = models.ImageField(
        upload_to=preview_image_dir_path,
        help_text='Detected pixels the brightness of which was changed more than "Detect Lev"',
        null=True, blank=True
    )
    long_term_avg_preview = models.ImageField(
        upload_to=preview_image_dir_path,
        help_text="Long term averaged brightness of the pixel.",
        null=True, blank=True
    )
    peak_hold_preview = models.ImageField(
        upload_to=preview_image_dir_path,
        help_text="Automatic composite still image which contains the peak brightness of each pixel "
                  "during the detection will be saved as a still image. "
                  "Peak hold is useful in nighttime luminous event observation. "
                  "Exclusive with SnapShot setting.",
        null=True, blank=True
    )

    map_filename = models.CharField(
        max_length=260,
        help_text='Filename of a file on the remote station. '
                  '*M.bmp which contains layered information of the event.',
        blank=True, null=True
    )
    clip_filename = models.CharField(
        max_length=260,
        help_text='Filename of a clip file on the remote station.',
        # blank=True, null=True
    )
    xml_filename = models.CharField(
        max_length=260,
        help_text='Filename of a xml file on the remote station. ',
        blank=True, null=True
    )
    type = models.CharField(
        max_length=3,
        choices=[
            ('rec', 'Recording'),
            ('trg', 'Trigger'),
            ('tmp', 'Temporary'),
        ],
        help_text='Type of the UFOCapture entry determined from the name of a file'
    )

    filename_datetime = models.DateTimeField(
        help_text='Datetime value derived from from UFOCapture file.',
        null=True
    )

    version = models.CharField(
        max_length=20,
        help_text='Value of attribute "version" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
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
        help_text='Value of attribute "tz" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
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
        blank=True, null=True
    )
    lid = models.CharField(
        max_length=16,
        help_text='Value of attribute "lid" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )
    observer = models.CharField(
        max_length=32,
        help_text='Value of attribute "observer" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )
    sid = models.CharField(
        max_length=16,
        help_text='Value of attribute "sid" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )
    cam = models.CharField(
        max_length=32,
        help_text='Value of attribute "cam" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )
    lens = models.CharField(
        max_length=32,
        help_text='Value of attribute "lens" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )
    cap = models.CharField(
        max_length=32,
        help_text='Value of attribute "cap" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )
    comment = models.CharField(
        max_length=64,
        help_text='Value of attribute "comment" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
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
    fourcc = models.CharField(
        max_length=16,
        help_text='Value of attribute "fourcc" of ufocapture_record inside UFOCapture XML file.',
        blank=True, null=True
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def __str__(self):
        model_name = self.__class__.__name__
        field_value_strs = []

        for field in ['clip_filename', 'type']:
            v = getattr(self, field)
            v_str = f'"{v}"' if isinstance(v, str) else v.name
            field_value_strs.append(f'{field}: {v_str}')

        return f'{model_name} ({", ".join(field_value_strs)})'
