import os.path

from django.apps import AppConfig


class RestServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rest_server'

    REPORT_BASE_DATA_DIR = os.path.join(
        # causes exception: validate_file_name, utils.py:17
        #   SuspiciousFileOperation("Detected path traversal attempt in ...
        # os.path.dirname(__file__), 'static',
        'report_data'
    )
    # see: https://stackoverflow.com/questions/1340776/secure-static-media-access-in-a-django-site
