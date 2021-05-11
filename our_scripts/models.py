from django.db import models
from time import sleep
from threading import Thread
import os
import django

from freebets.models import Event, Bet


# Create your models here.
class Player(models.Model):
    login = models.CharField("User Login", max_length=200)
    cash = models.IntegerField()

    def __str__(self):
        return self.login

