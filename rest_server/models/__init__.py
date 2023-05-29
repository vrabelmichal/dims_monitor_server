from django.db import models

from rest_server.models.report import Report

from rest_server.models.disk_usage import DiskUsage
from rest_server.models.disk_partition import DiskPartition
from rest_server.models.memory_usage import MemoryUsage
from rest_server.models.cpu_status import CpuStatus
from rest_server.models.ohm_measurement import \
    OhmHardwareInformation, OhmSensorParameter, OhmSensorInformation, OhmSensorMeasurement
from rest_server.models.ufo_capture_output import UfoCaptureOutputEntry
from rest_server.models.station import Station
from rest_server.models.env_log_measurement import EnvironmentLogUpload, EnvironmentLogMeasurement, EnvironmentLogType
from rest_server.models.process import Process
from rest_server.models.observing_station import ObservingStation
from rest_server.models.camera_status import CameraStatus
