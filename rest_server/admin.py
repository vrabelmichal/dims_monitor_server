from django.contrib import admin

from rest_server.models import Report, DiskPartition, DiskUsage

admin.site.register(Report)
admin.site.register(DiskPartition)
admin.site.register(DiskUsage)

admin.site.site_header = "DIMS REST Server Administration"
admin.site.site_title = "DIMS REST Server Administration"
admin.site.index_title = "Welcome to DIMS REST Server Administration"
