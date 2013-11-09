import json

from django.shortcuts import render
from django.http import HttpResponse

from food.models import Recipe, Food, Log

def get_log_totals(request):
    """
    Returns totals for a day (Log object)
    """
    log = Log.objects.get(id=request.GET['id'])
    totals = log.totals()
    resp = [{'label': 'Protein', 'value': totals['protein']},
            {'label': 'Carbs', 'value':  totals['carbs']}, 
            {'label': 'Fat', 'value': totals['fat']}]
    data = json.dumps(resp)
    return HttpResponse(data, content_type='application/json')

def get_foods_for_id(request):
    """
    Returns all Food objects for a Recipe id
    """
    recipe_id = request.GET['id']

    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = recipe.ingredient_set.all()
    resp = []
    for ingredient in ingredients:
        resp.append({
            'food_id': ingredient.food_id, 
            'amount': ingredient.amount,
            'unit': ingredient.unit,
        })
    data = json.dumps(resp)
    return HttpResponse(data, content_type='application/json')
