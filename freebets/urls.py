from django.urls import path

from . import views
app_name="freebets"
urlpatterns = [
    path('',views.index, name = 'index'),
    path('<int:event_id>/', views.event, name='event'),
    path('<int:event_id>/make_bet/', views.make_bet, name='make_bet')




]