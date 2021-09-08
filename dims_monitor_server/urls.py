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
from django.urls import path

import rest_server.views.index

import rest_server.views.report

import rest_server.views.disk_usage
from rest_server import views

urlpatterns = [
    path('', rest_server.views.index, name='index'),
    path('admin/', admin.site.urls),

    path('api/complex-reports/', rest_server.views.ComplexReportList.as_view()),

    path('api/reports/', rest_server.views.ReportList.as_view()),
    path('api/reports/<int:pk>/', rest_server.views.ReportDetail.as_view()),
    path('api/disk-usages/', rest_server.views.DiskUsageList.as_view()),
]
