from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Event(models.Model):
    event_name = models.CharField('Game name', max_length=200) # название матча например зенит-спартак
    event_date = models.DateTimeField('Game date') # дата события
    event_result = models.IntegerField() # 1 first team win - 2 second team win 0 - pari isnt finish yet
    # эти две переменные для расчёта коэфициента
    cash_to_first_team = models.IntegerField() # сколько денег поставили на первую команду
    cash_to_second_team = models.IntegerField() # на вторую команду

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

class User(models.Model):
    login = models.CharField('login',max_length=200)
    cash = models.IntegerField()
    registration = models.DateTimeField('Registration date')

    def __str__(self):
        return self.login
