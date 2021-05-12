from django.urls import path

from . import views
print ("Ready")

app_name="freebets"
urlpatterns = [
    path('',views.index, name = 'index'),
    path('<int:event_id>/', views.event, name='event'),
    path('<int:event_id>/make_bet/', views.make_bet, name='make_bet'),
    path('/no_money/', views.no_money, name='no_money'),
    path('/feel_cash/', views.feel_cash, name='feel_cash')





]