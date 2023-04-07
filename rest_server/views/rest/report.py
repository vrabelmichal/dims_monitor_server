import datetime
import json
import logging
import re
import traceback

from rest_framework import generics, status, permissions
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_server.models import Report, Station
from rest_server.serializers import ReportNestedSerializer


OPERATIONS_LOGGER = logging.getLogger('dims_monitor_server.rest_server.rest.report')

class HasCreateReportPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('rest_server.add_report')


class ComplexReportList(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        HasCreateReportPermission
    ]

    # monitor_name_serializer_mapping = dict(
    #     hdd_usage=DiskUsageSerializer,
    # )

    _attachments_re = re.compile(
        r'attachments\[(?P<monitor_name>\w+)\]\[(?P<measurement_i>\d+)\]\[(?P<file_k>\w+)\]'
    )

    _supported_compressions = ('zlib', 'none')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger('rest_server.ReportNestedSerializer')

    def post(self, request, format=None):
        # print(request)
        # user(=station) data could be acquired here

        for k in ['start_utc', 'post_utc', 'hash', 'data']:
            if k not in request.data:
                return Response(data=dict(status=f'Missing attribute {k}'), status=status.HTTP_400_BAD_REQUEST)

        users_station = None

        try:
            data_compression = None
            if 'compression' in request.data:
                if request.data['compression'] in self._supported_compressions:
                    data_compression = request.data['compression']

            try:
                request_data = request.data['data']

                if data_compression == 'zlib':
                    import zlib
                    from django.core.files.uploadedfile import UploadedFile
                    if not isinstance(request_data, UploadedFile):
                        raise RuntimeError('Unexpected request data')
                    request_data = request_data.read()
                    request_data = zlib.decompress(request_data).decode('utf8')

                measurements_dict = json.loads(request_data)
                del request_data

            except json.decoder.JSONDecodeError:
                return Response(data=dict(status=f'Cannot parse measurement data as JSON'), status=status.HTTP_400_BAD_REQUEST)

            attachments_dict = dict()

            for attr_a, attr_v in request.data.items():
                m = self._attachments_re.match(attr_a)
                if not m:
                    continue
                monitor_name = m.group('monitor_name')
                if monitor_name not in attachments_dict:
                    attachments_dict[monitor_name] = dict()
                str_measurement_i = m.group('measurement_i')
                if str_measurement_i not in attachments_dict[monitor_name]:
                    attachments_dict[monitor_name][str_measurement_i] = dict()
                file_k = m.group('file_k')
                attachments_dict[monitor_name][str_measurement_i][file_k] = attr_v

            if len(attachments_dict) > 0:
                measurements_dict['attachments'] = attachments_dict

            users_station, users_station_created = Station.objects.get_or_create(name=request.user.username)

            rns_data = dict(
                start_utc=request.data['start_utc'],
                post_utc=request.data['post_utc'],
                hash=request.data['hash'],
                retrieved_utc=datetime.datetime.utcnow(),  # !!!! suspicious
                station=users_station.name,
                **measurements_dict
            )

            rns = ReportNestedSerializer(data=rns_data)
            # existing hash might cause problems here

            # try:

            if rns.is_valid(raise_exception=True):
                rns.save()
                return Response(data=dict(status='Created'), status=status.HTTP_201_CREATED)

        except Exception as e:
            OPERATIONS_LOGGER.warning(
                'Exception caught while handling post request. '
                'Request by: %s (station: %s). '
                'Report start_utc: %s, post_utc: %s, hash: %s. '
                'Exception %s: %s. '
                'Traceback: %s',
                request.user.username, users_station.name if users_station is not None else 'None',
                str(request.data['start_utc']), str(request.data['post_utc']), str(request.data['hash']),
                e.__class__.__name__, str(e),
                traceback.format_exc()
            )
            return Response({e.__class__.__name__: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(rns.errors, status=status.HTTP_400_BAD_REQUEST)
