from django.contrib import admin

from rest_server.models import DiskPartition, DiskUsage, CpuStatus, OhmSensorMeasurement, OhmHardwareInformation, \
    OhmSensorInformation, OhmSensorParameter, UfoCaptureOutputEntry
from rest_server.models import Report

admin.site.register(Report)
admin.site.register(DiskPartition)
admin.site.register(DiskUsage)
admin.site.register(CpuStatus)
admin.site.register(OhmSensorMeasurement)
admin.site.register(OhmHardwareInformation)
admin.site.register(OhmSensorInformation)
admin.site.register(OhmSensorParameter)
admin.site.register(UfoCaptureOutputEntry)

admin.site.site_header = "DIMS REST Server Administration"
admin.site.site_title = "DIMS REST Server Administration"
admin.site.index_title = "Welcome to DIMS REST Server Administration"
