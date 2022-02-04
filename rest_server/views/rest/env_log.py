from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_server.models import EnvironmentLogMeasurement, EnvironmentLogUpload


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def latest_env_log_measurement(request):
    station = request.user

    env_log_entries_set = EnvironmentLogMeasurement.objects \
        .filter(station__name=station) \
        .order_by('-measurement_datetime')[:1]

    if env_log_entries_set.count() > 0:
        latest_entry = env_log_entries_set[0]

        return Response({
            k: latest_entry.__dict__[k]
            for k in latest_entry.__dict__.keys()
            if not k.startswith('_')
        })

    return Response(status=204)


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def latest_env_log_upload(request):
    station = request.user

    env_log_entries_set = EnvironmentLogUpload.objects \
        .filter(station__name=station) \
        .order_by('-captured_hour')[:1]

    if env_log_entries_set.count() > 0:
        latest_entry = env_log_entries_set[0]

        return Response({
            k: latest_entry.__dict__[k]
            for k in latest_entry.__dict__.keys()
            if not k.startswith('_')
        })

    return Response(status=204)
