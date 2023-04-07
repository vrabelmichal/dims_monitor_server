"""dims_monitor_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from dims_monitor_server import settings
from django.conf.urls.static import static
from django.views.static import serve

import rest_server.views.web
import rest_server.views.rest

urlpatterns = [
    path('', rest_server.views.web.latest_reports, name='latest_reports'),
    path('latest-reports-with-events', rest_server.views.web.latest_reports_with_events, name='latest_reports_with_events'),
    path('ufo-thumbnails-maintenance', rest_server.views.web.ufo_thumbnails_maintenance, name='ufo_thumbnails_maintenance'),
    path('test', rest_server.views.web.test, name='test'),
    path('report/<int:report_id>', rest_server.views.web.report_detail, name='report_detail'),
    path('accounts/', include('django.contrib.auth.urls')),

    re_path(r'^favicon\.ico$', serve, kwargs=dict(
        document_root=settings.BASE_DIR / 'rest_server' / 'static',
        path='favicon.ico'
    )),

    path('admin/', admin.site.urls),

    path('api/complex-reports/', rest_server.views.rest.ComplexReportList.as_view()),

    # path('api/reports/', rest_server.views.rest.ReportList.as_view()),
    # path('api/reports/<int:pk>/', rest_server.views.rest.ReportDetail.as_view()),
    # path('api/disk-usages/', rest_server.views.rest.DiskUsageList.as_view()),
    path('api/ufo-capture-output/latest', rest_server.views.rest.latest_ufo_capture_file),
    path('api/environment-log-upload/latest', rest_server.views.rest.latest_env_log_upload),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
