from django.contrib import admin

# Register your models here.
from .models import Event, Bet

admin.site.register(Event)
admin.site.register(Bet)