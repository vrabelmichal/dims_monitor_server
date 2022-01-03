from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')  # getting our template
    return HttpResponse(template.render())  # rendering the template in HttpResponse

    # return HttpResponse("Dashboard")