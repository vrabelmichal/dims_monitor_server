import datetime
import json

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
