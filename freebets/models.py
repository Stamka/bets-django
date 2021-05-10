from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Event(models.Model):
    event_name = models.CharField('Game name', max_length=200)
    event_date = models.DateTimeField('Game date')

    def __str__(self):
        return self.event_name

    def is_event_over(self):  # fix ittt
        return self.event_date >= (self.event_date - timezone.now())


class Bet(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    eventBet = models.CharField('pari', max_length=200)
    dollars = models.IntegerField('bet amount')
    date_added = models.DateTimeField('bet date')

    def __str__(self):
        return self.eventBet
