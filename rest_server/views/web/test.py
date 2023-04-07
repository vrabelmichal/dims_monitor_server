import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

THUMB_MAINTENANCE_LOGGER = logging.getLogger('dims_monitor_server.rest_server.web.test')

@login_required
def test(request):
    logger = THUMB_MAINTENANCE_LOGGER

    for i in range(2):
        logger.info(
            'TEST %d', i
        )

    template = loader.get_template('test.html')  # getting our template

    return HttpResponse(template.render(
        dict(
            segment='test',
        ),
        request
    ))