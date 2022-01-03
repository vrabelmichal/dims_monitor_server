from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_server.models.ufo_capture_output import UfoCaptureOutputEntry


@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def latest_ufo_capture_file(request):
    station = request.user

    ufo_capture_entries_set = UfoCaptureOutputEntry.objects \
        .filter(report__station=station) \
        .order_by('-filename_datetime')[:1]

    if ufo_capture_entries_set.count() > 0:
        latest_entry = ufo_capture_entries_set[0]

        return Response({
            k: latest_entry.__dict__[k]
            for k in latest_entry.__dict__.keys()
            if not k.startswith('_')
        })

    return Response(status=204)

    # Report.objects.all()
    # <QuerySet [<Report: Station status report (station: "dims_0", measurement started at: 2021-09-07 07:46:30.937461+00:00, data hash: -8524034808760250428)>, <Report: Station status report (station: "dims_0", measurement started at: 2021-09-07 08:03:05.109048+00:00, data hash: -1262448447693268149)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-09-07 13:06:03.546792+00:00, data hash: 2695044024533283280)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-09-08 11:36:45.120509+00:00, data hash: 602663221240429583)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-09-08 11:38:32.235905+00:00, data hash: 8672048216604262167)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-09-08 11:40:34.153885+00:00, data hash: 6372637306054228063)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 19:48:06.437104+00:00, data hash: 8225439704213503822)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 20:16:36.166313+00:00, data hash: -3540738125319724809)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 20:17:52.695546+00:00, data hash: 2110808299046167703)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 20:18:26.272675+00:00, data hash: 6796223061703567713)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:00:16.294421+00:00, data hash: -7900506793643976745)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:02:26.606048+00:00, data hash: 6859124324865798843)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:04:14.862838+00:00, data hash: 6166381159658857408)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:07:54.429188+00:00, data hash: -9095366147131108468)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:23:31.092543+00:00, data hash: -8315768525227222675)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:34:44.537760+00:00, data hash: 5869466967585965015)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:35:26.423495+00:00, data hash: -636587186344649891)>, <Report: Station status report (station: "test_machine", measurement started at: 2021-10-19 21:36:03.743400+00:00, data hash: -7502780367320599826)>, <Report: Station status report (station: "test_machine_2", measurement started at: 2021-10-20 05:59:57.932375+00:00, data hash: 875607037883673749)>, <Report: Station status report (station: "test_machine_2", measurement started at: 2021-10-20 06:02:14.958685+00:00, data hash: 3184042871750308174)>, '...(remaining elements truncated)...']>
    # Report.objects.order_by('-start_utc')[0]
    # <Report: Station status report (station: "test_machine", measurement started at: 2021-10-29 10:38:57.451494+00:00, data hash: -7071631145523976328)>
    # Report.objects.order_by('start_utc')[0]
    # <Report: Station status report (station: "dims_0", measurement started at: 2021-09-07 07:46:30.937461+00:00, data hash: -8524034808760250428)>
    # Report.objects.order_by('-start_utc')[0]
    # <Report: Station status report (station: "test_machine", measurement started at: 2021-10-29 10:38:57.451494+00:00, data hash: -7071631145523976328)>


