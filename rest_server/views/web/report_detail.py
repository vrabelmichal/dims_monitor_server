import django.db
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from rest_server.models import Report, CpuStatus, DiskUsage, MemoryUsage, OhmSensorMeasurement, UfoCaptureOutputEntry, \
    EnvironmentLogMeasurement, EnvironmentLogUpload, Process


@login_required
def report_detail(request, report_id):
    report = Report.objects.filter(id=report_id).first()

    cpu_status = CpuStatus.objects.filter(report_id=report_id)
    disk_usage = DiskUsage.objects.filter(report_id=report_id)
    memory_usage = MemoryUsage.objects.filter(report_id=report_id)
    ohm = OhmSensorMeasurement.objects.filter(report_id=report_id)
    ufo_caputre_output = UfoCaptureOutputEntry.objects.filter(report_id=report_id)

    max_count_of_latest_environment_log_measurements = 10

    subqry = django.db.models.Subquery(
        EnvironmentLogMeasurement.objects
            .filter(log_upload_id=django.db.models.OuterRef('log_upload_id'))
            .order_by('-measurement_datetime')
            .values_list('id', flat=True)[:max_count_of_latest_environment_log_measurements]
    )

    environment_log = EnvironmentLogUpload.objects.filter(report_id=report_id).prefetch_related(
        django.db.models.Prefetch(
            'environmentlogmeasurement_set',
            to_attr='measurements',
            queryset=EnvironmentLogMeasurement.objects.filter(id__in=subqry)
                .order_by('measurement_datetime')
        )
    )

    processes = Process.objects.filter(report_id=report_id).order_by('-cpu_percent')

    template = loader.get_template('report_details.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            report=report,
            cpu_status=cpu_status,
            disk_usage=disk_usage,
            memory_usage=memory_usage,
            ohm=ohm,
            ufo_caputre_output=ufo_caputre_output,
            environment_log=environment_log,
            processes=processes,
            max_count_of_latest_environment_log_measurements=max_count_of_latest_environment_log_measurements,
            segment='report_detail',
        ),
        request
    ))
