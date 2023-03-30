from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dims_monitor_server.settings')

app = Celery('dims_monitor_server')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# print('-'*100)
# from pprint import pprint
# pprint('Celery config:')
# print(app._conf)
# print('-'*100)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
