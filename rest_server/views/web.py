from django.http import HttpResponse
from django.template import loader
from django.core import serializers

from rest_server.models import Station, Report, DiskUsage, CpuStatus, MemoryUsage, OhmSensorMeasurement, \
    UfoCaptureOutputEntry


def index(request):

    stations = Station.objects.all()
    latest_reports_per_station = dict()
    count_ufo_outputs_per_station = dict()
    for station in stations:
        latest_reports_per_station[station.name] = \
            Report.objects.filter(station=station).order_by('-start_utc')[:10]
        count_ufo_outputs_per_station[station.name] = {
            report.id: UfoCaptureOutputEntry.objects.filter(report=report).all().count()
                for report in latest_reports_per_station[station.name]
        }

    template = loader.get_template('index.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            stations=stations,
            latest_reports_per_station=latest_reports_per_station,
            count_ufo_outputs_per_station=count_ufo_outputs_per_station
        ),
        request
    ))  # rendering the template in HttpResponse


def report_detail(request, report_id):
    report = Report.objects.filter(id=report_id).first()

    cpu_status = CpuStatus.objects.filter(report_id=report_id)
    disk_usage = DiskUsage.objects.filter(report_id=report_id)
    memory_usage = MemoryUsage.objects.filter(report_id=report_id)
    ohm = OhmSensorMeasurement.objects.filter(report_id=report_id)
    ufo_caputre_output = UfoCaptureOutputEntry.objects.filter(report_id=report_id)

    # ufo_caputre_output_data = serializers.serialize("python", ufo_caputre_output.all())


    template = loader.get_template('report_details.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            report=report,
            cpu_status=cpu_status,
            disk_usage=disk_usage,
            memory_usage=memory_usage,
            ohm=ohm,
            ufo_caputre_output=ufo_caputre_output,
            # ufo_caputre_output_data=ufo_caputre_output_data
        ),
        request
    ))