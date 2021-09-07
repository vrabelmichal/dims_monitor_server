import json

from django.http import Http404
from django.shortcuts import render
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import generics

from rest_server.models import Report, DiskUsage
from rest_server.serializers import ReportSerializer, DiskUsageSerializer, ReportNestedSerializer


def index(request):
    return HttpResponse("Dashboard")


class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # not really needed


class DiskUsageList(generics.ListCreateAPIView):
    queryset = DiskUsage.objects.all()
    serializer_class = DiskUsageSerializer


class ComplexReportList(APIView):

    # monitor_name_serializer_mapping = dict(
    #     hdd_usage=DiskUsageSerializer,
    # )

    def post(self, request, format=None):
        # print(request)
        # user(=station) data could be acquired here

        for k in ['start_utc', 'hash', 'data']:
            if k not in request.data:
                return Response(data=dict(status=f'Missing attribute {k}'), status=status.HTTP_400_BAD_REQUEST)
        try:
            measurements_dict = json.loads(request.data['data'])
        except json.decoder.JSONDecodeError:
            return Response(data=dict(status=f'Cannot parse measurement data as JSON'), status=status.HTTP_400_BAD_REQUEST)

        rns_data = dict(
            start_utc=request.data['start_utc'],
            hash=request.data['hash'],
            station='dims_0', # TODO
            **measurements_dict
        )

        rns = ReportNestedSerializer(data=rns_data)

        if rns.is_valid():
            rns.save()
            return Response(rns.data, status=status.HTTP_201_CREATED)
            # return Response(data=dict(status='Success'), status=status.HTTP_201_CREATED)

        return Response(rns.errors, status=status.HTTP_400_BAD_REQUEST)

        # repser = ReportSerializer(data=dict(
        #     start_utc=request['start_utc'],
        #     station='USER',#request['station']
        #     hash=request['hash'],
        # ))
        #
        #
        # for monitor_name in measurements_dict:
        #     pass
        #
        # pass
        # return Response(data=dict(status='Success'), status=status.HTTP_201_CREATED)