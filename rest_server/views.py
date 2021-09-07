import json

from django.http import Http404
from django.shortcuts import render
from rest_framework import status, mixins, generics
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import generics

from rest_server.models import Report, DiskUsage
from rest_server.serializers import ReportSerializer, DiskUsageSerializer, ReportNestedSerializer


def index(request):
    return HttpResponse("Dashboard")


class ReportList(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    # not really needed


class DiskUsageList(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = DiskUsage.objects.all()
    serializer_class = DiskUsageSerializer


class ComplexReportList(APIView):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
            station=request.user.username, #'dims_0', # TODO
            **measurements_dict
        )

        rns = ReportNestedSerializer(data=rns_data)

        if rns.is_valid():
            rns.save()
            return Response(data=dict(status='Success'), status=status.HTTP_201_CREATED)
            # return Response(data=dict(status='Success'), status=status.HTTP_201_CREATED)

        return Response(rns.errors, status=status.HTTP_400_BAD_REQUEST)


# https://www.django-rest-framework.org/api-guide/parsers/#fileuploadparser

# # views.py
# class FileUploadView(views.APIView):
#     parser_classes = [FileUploadParser]
#
#     def put(self, request, filename, format=None):
#         file_obj = request.data['file']
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(status=204)
#
# # urls.py
# urlpatterns = [
#     # ...
#     re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
# ]
