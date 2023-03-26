import django.db
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from rest_server.models import Station, Report, UfoCaptureOutputEntry


@login_required
def latest_reports(request):

    stations = Station.objects.all().order_by('-priority')
    latest_reports_per_station = dict()
    count_ufo_outputs_per_station = dict()
    for station in stations:
        latest_reports_per_station[station.name] = \
            Report.objects.filter(station=station).order_by('-start_utc')[:10]

        # TODO this is inefficient

        count_ufo_outputs_per_station[station.name] = {
            report.id: UfoCaptureOutputEntry.objects.filter(report=report).all().count()
                for report in latest_reports_per_station[station.name]
        }

    template = loader.get_template('latest_records_tables.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            stations=stations,
            latest_reports_per_station=latest_reports_per_station,
            count_ufo_outputs_per_station=count_ufo_outputs_per_station,
            segment='latest_reports'
        ),
        request
    ))  # rendering the template in HttpResponse


@login_required
def latest_reports_with_events(request):

    stations = Station.objects.all().order_by('-priority')
    latest_reports_per_station = dict()
    count_ufo_outputs_per_station = dict()
    for station in stations:
        latest_reports_per_station[station.name] = \
            Report.objects.filter(station=station).annotate(
                django.db.models.Count('ufocaptureoutputentry')
            ).filter(ufocaptureoutputentry__count__gt=0).order_by('-start_utc')[:10]

        count_ufo_outputs_per_station[station.name] = {
            report.id: report.ufocaptureoutputentry__count
                for report in latest_reports_per_station[station.name]
        }

    template = loader.get_template('latest_records_tables.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            stations=stations,
            latest_reports_per_station=latest_reports_per_station,
            count_ufo_outputs_per_station=count_ufo_outputs_per_station,
            segment='latest_reports_with_events'
        ),
        request
    ))  # rendering the template in HttpResponse
