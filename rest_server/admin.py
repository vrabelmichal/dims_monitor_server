from django.contrib import admin

from rest_server.models import Report, DiskPartition, DiskUsage

admin.site.register(Report)
admin.site.register(DiskPartition)
admin.site.register(DiskUsage)
