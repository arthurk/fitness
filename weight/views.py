from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

from weight.models import Log

def get_all_bodyweight_numbers(request):
    """
    Returns all bodyweight numbers
    """
    weights = [n.bodyweight for n in Log.objects.all()]
    data = simplejson.dumps(weights)
    return HttpResponse(data, mimetype='application/json')
