from django.shortcuts import render
from .models import Event,Bet
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
def index(request):
    new_bets_list = Event.objects.order_by('-event_date')
    return render(request, 'bets.html',{'new_bets':new_bets_list})

def event(request, event_id):
    try:
        a=Event.objects.get( id = event_id)
    except:
        raise Http404("Такого матча нет")

    latest_bets = a.bet_set.order_by('-id')[:10]

    return render(request, 'event.html', {'event': a, 'latest_bets' : latest_bets })

def make_bet(request, event_id):
    try:
        a=Event.objects.get( id = event_id)
    except:
        raise Http404("Такого матча нет")

    eventBet = request.POST['team']
    dollars = request.POST['money']
    date_added = timezone.now()
    if not int(dollars) <= 0:
        a.bet_set.create (eventBet,dollars,date_added)
        return HttpResponseRedirect( reverse ('freebets:event', args=(a.id,)))
    else:
        raise Http404 (("BAN!!!"*100+"\n")*100)

