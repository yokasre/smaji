import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def dashboard(request) -> HttpResponse:
    template = loader.get_template('dashboard.html')
    api_url: str = "http://localhost:8000//analytics/get-current-water-level"
    response = requests.get(api_url, params={'tank_number': 10})
    data = response.json()
    context = {
        'current_level': data['level'],
        'percentage': data['percentage'],
    }

    return HttpResponse(template.render(context, request))
