import json

from django.http import HttpResponse

from food.models import Recipe, Food


def get_food(request):
    """
    Returns a JSON serialized Food object for ID
    """
    food_id = request.GET['id']
    food = Food.objects.select_related('serving').get(id=food_id)
    data = {
        'id': food.id,
        'unit': food.unit,
        'servings': [{'id': s.id, 'name': s.name, 'amount': s.amount,
                      'unit': s.unit}
                     for s in food.serving_set.all()]
    }
    return HttpResponse(json.dumps([data]), content_type='application/json')


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
