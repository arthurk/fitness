from datetime import date

from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Log(models.Model):
    day = models.DateField(default=date.today)
    desc = models.CharField(max_length=100, blank=True, null=True)
    exercises = models.ManyToManyField(Exercise, through='Set')

    def __unicode__(self):
        return str(self.day)

class Set(models.Model):
    log = models.ForeignKey(Log)
    exercise = models.ForeignKey(Exercise)
    weight = models.IntegerField()
    reps = models.IntegerField()

    def __unicode__(self):
        return str('%s %sx%s' % (self.exercise,
                                self.weight,
                                self.reps))
