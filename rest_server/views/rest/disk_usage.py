from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_server.models import DiskUsage
from rest_server.serializers import DiskUsageSerializer


class DiskUsageList(generics.ListCreateAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = DiskUsage.objects.all()
    serializer_class = DiskUsageSerializer