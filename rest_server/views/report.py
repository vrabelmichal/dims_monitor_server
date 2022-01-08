import datetime
import json
import re

from rest_framework import generics, status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_server.models import Report
from rest_server.serializers import ReportNestedSerializer


class ComplexReportList(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # monitor_name_serializer_mapping = dict(
    #     hdd_usage=DiskUsageSerializer,
    # )

    _attachments_re = re.compile(
        r'attachments\[(?P<monitor_name>\w+)\]\[(?P<measurement_i>\d+)\]\[(?P<file_k>\w+)\]'
    )

    def post(self, request, format=None):
        # print(request)
        # user(=station) data could be acquired here
        pass
        for k in ['start_utc', 'post_utc', 'hash', 'data']:
            if k not in request.data:
                return Response(data=dict(status=f'Missing attribute {k}'), status=status.HTTP_400_BAD_REQUEST)
        try:
            measurements_dict = json.loads(request.data['data'])
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

        rns_data = dict(
            start_utc=request.data['start_utc'],
            post_utc=request.data['post_utc'],
            hash=request.data['hash'],
            retrieved_utc=datetime.datetime.utcnow(),
            station=request.user.username,
            **measurements_dict
        )

        rns = ReportNestedSerializer(data=rns_data)
        # existing hash might cause problems here

        # try:

        if rns.is_valid(raise_exception=True):
            rns.save()
            return Response(data=dict(status='Created'), status=status.HTTP_201_CREATED)

        # except ValidationError as e:
        #     print(e.detail)
            # print(e.detail['hash'])
            # print(e.detail['hash'][0].code)
            # pass

        return Response(rns.errors, status=status.HTTP_400_BAD_REQUEST)
