from datetime import date

from django.db import models

UNIT_CHOICES = (
    ('KG', 'kg'),
)

class Log(models.Model):
    day = models.DateField(default=date.today)
    bodyweight = models.IntegerField()
    unit = models.CharField(max_length=2,
                            choices=UNIT_CHOICES,
                            default=UNIT_CHOICES[0])

    def __unicode__(self):
        return str(self.day)
