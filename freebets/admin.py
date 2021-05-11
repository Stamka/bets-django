from django.contrib import admin

# Register your models here.
from .models import Event, Bet, User

admin.site.register(Event)
admin.site.register(Bet)
admin.site.register(User)