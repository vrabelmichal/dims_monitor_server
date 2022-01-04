from django.db import models

from rest_server.models.report import Report

from rest_server.models.disk_usage import DiskPartition, DiskUsage
from rest_server.models.memory_usage import MemoryUsage
from rest_server.models.cpu_status import CpuStatus
from rest_server.models.ohm_measurement import \
    OhmHardwareInformation, OhmSensorParameter, OhmSensorInformation, OhmSensorMeasurement
from rest_server.models.ufo_capture_output import UfoCaptureOutputEntry
from rest_server.models.station import Station
