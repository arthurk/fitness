import json

from django.shortcuts import render
from django.http import HttpResponse

from food.models import Recipe, Food

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