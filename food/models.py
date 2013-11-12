from __future__ import division
from datetime import date

from django.db import models

UNIT_CHOICES = (
    ('MG', 'mg'),
    ('G', 'g'),
    ('ML', 'ml'),
    ('L', 'l'),
)

class Food(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField(default=100)
    unit = models.CharField(max_length=2,
                            choices=UNIT_CHOICES,
                            default=UNIT_CHOICES[0])
    kcal = models.IntegerField()

    # macros
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    # todo: add fiber

    # minerals
    """
    calcium = models.IntegerField(blank=True, null=True)
    iron = models.IntegerField(blank=True, null=True)
    magnesium = models.IntegerField(blank=True, null=True)
    phosphorus = models.IntegerField(blank=True, null=True)
    potassium = models.IntegerField(blank=True, null=True)
    sodium = models.IntegerField(blank=True, null=True)
    zinc = models.IntegerField(blank=True, null=True)
    """

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Serving(models.Model):
    """
    Serving for a Food
    For example "1 Tablespoon Sugar" -> "15g Sugar"
    """
    food = models.ForeignKey(Food)
    name = models.CharField(max_length=200)
    amount = models.IntegerField(default=100)

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    foods = models.ManyToManyField(Food, through='Ingredient')
    desc = models.TextField(blank=True, null=True)

    def totals(self):
        "Return total kcal and macros"
        total = dict(kcal=0, protein=0, carbs=0, fat=0)
        for ingredient in self.ingredient_set.all():
            food = ingredient.food
            multiplier = (ingredient.amount / food.amount) 
            total['kcal'] += multiplier * food.kcal
            total['protein'] += multiplier * food.protein
            total['carbs'] += multiplier * food.carbs
            total['fat'] += multiplier * food.fat
        return total

    def __unicode__(self):
        return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    food = models.ForeignKey(Food)
    amount = models.IntegerField()
    unit = models.CharField(max_length=2,
                            choices=UNIT_CHOICES,
                            default=UNIT_CHOICES[0])

class Log(models.Model):
    day = models.DateField(default=date.today)
    foods = models.ManyToManyField(Food, through='FoodLog')

    def totals(self):
        "Returns totals for the day"
        total = dict(kcal=0, protein=0, carbs=0, fat=0)
        for foodlog in self.foodlog_set.all():
            food = foodlog.food
            multiplier = (foodlog.amount / food.amount) 
            total['kcal'] += multiplier * food.kcal
            total['protein'] += multiplier * food.protein
            total['carbs'] += multiplier * food.carbs
            total['fat'] += multiplier * food.fat
        return total
    
    def __unicode__(self):
        return str(self.day)

class FoodLog(models.Model):
    log = models.ForeignKey(Log)
    food = models.ForeignKey(Food)
    amount = models.IntegerField()
    unit = models.CharField(max_length=2)

    def totals(self):
        "Returns totals"
        total = dict(kcal=0, protein=0, carbs=0, fat=0)
        food = self.food
        multiplier = (self.amount / food.amount) 
        total['kcal'] = multiplier * food.kcal
        total['protein'] = multiplier * food.protein
        total['carbs'] = multiplier * food.carbs
        total['fat'] = multiplier * food.fat
        return total

    def __unicode__(self):
        return '%s%s %s' % (self.amount, self.unit, self.food)

