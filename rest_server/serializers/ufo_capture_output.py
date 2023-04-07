from rest_framework import serializers

from rest_server.models import Report, UfoCaptureOutputEntry, Station


class UfoCaptureOutputNestedSerializer(serializers.ModelSerializer):

    # not required for validation
    # report is presumed to be already existing before the creation of ufo capture output entry
    # read_only=False is necessary for values to be available in validated_data parameter of `create(...)` method

    report = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Report.objects.all()
    )

    station = serializers.PrimaryKeyRelatedField(
        many=False, read_only=False, required=False,
        queryset=Station.objects.all()
    )

    class Meta:
        model = UfoCaptureOutputEntry
        fields = '__all__'

    def create(self, validated_data):

        if 'report' not in validated_data:
            raise RuntimeError('Field "report" is required for the creation')

        return UfoCaptureOutputEntry.objects.create(
            **validated_data
        )


def short_description_of_data(data, keys=('clip_filename',)):
    return ",".join([f'{k}:"{str(data[k])}"' for k in keys if k in data])


# All fields except "station"
# "station" is taken from the report(
#             'snapshot_filename',
#             'peak_hold_filename',
#             'thumbnail_filename',
#             'internal_thumbnail_pathname',
#             'map_filename',
#             'clip_filename',
#             'xml_filename',
#             'type',
#             'filename_datetime',
#             'version',
#             'xml_datetime',
#             'trig',
#             'frames',
#             'lng',
#             'lat',
#             'alt',
#             'tz',
#             'u2',
#             'cx',
#             'cy',
#             'fps',
#             'head',
#             'tail',
#             'diff',
#             'sipos',
#             'sisize',
#             'dlev',
#             'dsize',
#             'countrycode',
#             'lid',
#             'observer',
#             'sid',
#             'cam',
#             'lens',
#             'cap',
#             'comment',
#             'interlace',
#             'bbf',
#             'dropframe',
#             'fourcc',
#             'report',
#         )
