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
    """
    A Food object
    For example "Oats"
    """
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
    unit = models.CharField(max_length=2,
                            choices=UNIT_CHOICES,
                            default=UNIT_CHOICES[0])

    def __unicode__(self):
        return "%s %s (%s)" % (self.name, self.food, self.amount)


class Recipe(models.Model):
    """
    A Recipe is a collection of Foods
    """
    name = models.CharField(max_length=200)
    foods = models.ManyToManyField(Food, through='Ingredient')
    desc = models.TextField(blank=True, null=True)

    def totals(self):
        "Return total kcal and macros"
        total = dict(kcal=0, protein=0, carbs=0, fat=0)
        for ingredient in self.ingredient_set.select_related('food').all():
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
    """
    An Ingredient is a Food used in a Recipe
    """
    recipe = models.ForeignKey(Recipe)
    food = models.ForeignKey(Food)
    amount = models.IntegerField()
    unit = models.CharField(max_length=2,
                            choices=UNIT_CHOICES,
                            default=UNIT_CHOICES[0])


class Log(models.Model):
    """
    Tracks all the foods eaten on a specific day
    """
    day = models.DateField(default=date.today)
    foods = models.ManyToManyField(Food, through='FoodLog')

    def totals(self):
        "Returns totals for the day"
        total = dict(kcal=0, protein=0, carbs=0, fat=0)
        for foodlog in self.foodlog_set.select_related('food').all():
            food = foodlog.food
            multiplier = (foodlog.amount / food.amount)
            total['kcal'] += multiplier * food.kcal
            total['protein'] += multiplier * food.protein
            total['carbs'] += multiplier * food.carbs
            total['fat'] += multiplier * food.fat
        return total

    def __unicode__(self):
        return str(self.day)

    class Meta:
        ordering = ('-day',)


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


class Objective(models.Model):
    """
    An Objective is a group of targets
    """
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True)

    def is_active(self):
        """
        Returns a boolean indicating if the Objective is active (according to
        the start/end_date)
        """
        today = date.today()
        if self.end_date:
            active = self.start_date <= today <= self.end_date
        else:
            active = self.start_date <= today
        return active

    def __unicode__(self):
        return str(self.name)

    class Meta:
        ordering = ('-start_date',)

NAME_CHOICES = (
    ('KC', 'kcal'),
    ('PR', 'protein'),
    ('CA', 'carbs'),
    ('FA', 'fat'),
)

TARGET_CHOICES = (
    ('G', 'greater than'),
    ('B', 'between'),
    ('L', 'less than'),
)


class Target(models.Model):
    """
    A specific target (e.g. kcal <= 2000)
    """
    objective = models.ForeignKey(Objective)
    name = models.CharField(max_length=2,
                            choices=NAME_CHOICES,
                            default=NAME_CHOICES[0])
    goal = models.CharField(max_length=1,
                            choices=TARGET_CHOICES,
                            default=TARGET_CHOICES[0])
    value = models.IntegerField()
    # only used when "between" is selected
    value2 = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        names = dict(NAME_CHOICES)
        goals = dict(TARGET_CHOICES)
        if self.goal == 'B':
            return "%s %s %s and %s" % (names[self.name], goals[self.goal],
                                        self.value, self.value2)
        else:
            return '%s %s %s' % (names[self.name], goals[self.goal],
                                 self.value)
