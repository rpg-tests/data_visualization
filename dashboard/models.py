from django.core.validators import MinValueValidator
from django.db import models


class Reservation(models.Model):
    hotel_id = models.BigIntegerField(validators=[MinValueValidator(1)])
    total = models.IntegerField(validators=[MinValueValidator(0)])

    PERIOD_DAILY = 'day'
    PERIOD_MONTHLY = 'month'
    PERIOD_YEARLY = 'year'
    PERIOD_CHOICES = (
        (PERIOD_DAILY, 'Daily'),
        (PERIOD_MONTHLY, 'Monthly'),
        (PERIOD_YEARLY, 'Yearly'),
    )
    period_type = models.CharField(choices=PERIOD_CHOICES)

    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
