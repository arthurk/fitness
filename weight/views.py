import json

from django.shortcuts import render
from django.http import HttpResponse

from weight.models import Log

def get_all_bodyweight_numbers(request):
    """
    Returns all bodyweight numbers
    """
    weights = [n.bodyweight for n in Log.objects.all()]
    data = json.dumps(weights)
    return HttpResponse(data, mimetype='application/json')
