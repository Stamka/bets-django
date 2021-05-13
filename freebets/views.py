from django.shortcuts import render
from .models import Event,Bet, User
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
def index(request):
    new_bets_list = Event.objects.order_by('-event_date')
    user =User.objects.get(id= 1)
    return render(request, 'bets.html',{'new_bets':new_bets_list, 'user':user})

def no_money(request):
    return render(request, 'no_money.html')

def event(request, event_id, alert=0):
    user = User.objects.get(id=1)
    try:
        a=Event.objects.get( id = event_id)
    except:
        raise Http404("Такого матча нет")
    # расчёт коэфа на ставку
    cash1 = a.cash_to_first_team
    cash2 = a.cash_to_second_team

    if cash1 == cash2:
        kef1=2
        kef2=2
    else:
        s = cash1+cash2
        print(cash1, cash2, s)
        try:
            kef1 = 1 /(cash1/s)
        except:
            kef1 = 1 / (0.001 /s)
        try:
            kef2 = 1 / (cash2/s)
        except:
            kef2 = 1 / (0.001 /s)
        if (kef2>10):
            kef2=10
        kef1 = float('{:.2f}'.format(kef1))
        kef2 = float('{:.2f}'.format(kef2))
    latest_bets = a.bet_set.order_by('-id')[:10]
    
    if a.event_result != 0:
        if a.event_result == 1:
            for i in a.bet_set.all():
                if i.eventBet == "first":
                    if cash1 >= int(i.dollars * kef1):
                        user.cash += int(i.dollars * kef1)
                        user.save()
                        a.cash_to_first_team -= int(i.dollars * kef1)
                        a.save()
        if a.event_result == 2:
            for i in a.bet_set.all():
                if i.eventBet == "second":
                    if cash1 >= int(i.dollars * kef2):
                        user.cash += int(i.dollars * kef2)
                        user.save()
                        a.cash_to_second_team -= int(i.dollars * kef1)
                        a.save()
                

    return render(request, 'event.html', {'event': a, 'latest_bets' : latest_bets, 'user': user,
                                          'k1': kef1,'k2': kef2,'cash1':cash1,'cash2': cash2 })

def feel_cash(request):
    b = User.objects.get(id=1)
    dollars = request.POST['feel_money']
    if int(dollars) >= 0:
        b.cash +=int( dollars)
        b.save()
        return HttpResponseRedirect(reverse('freebets:index'))
    else:
        raise Http404(("BAN!!!" * 100 + "\n") * 100)

def make_bet(request, event_id):
    try:
        a=Event.objects.get( id = event_id)

    except:
        raise Http404("Такого матча нет")
    #if a.event_result != 0:
     #   raise Http404("Матч закончен")

    b = User.objects.get(id=1)
    dollars = request.POST['money']
    if (int(dollars) > b.cash):
        return HttpResponseRedirect(reverse('freebets:no_money', args=()))
    else:
        if not int(dollars) <= 0 :
            b.cash-=int(dollars)
            b.save()
            eventBet = request.POST['team']
            if eventBet == "first":
                a.cash_to_first_team += int(dollars)
            else:
                a.cash_to_second_team += int(dollars)
            a.save()
            a.bet_set.create(eventBet = request.POST['team'], dollars = request.POST['money'], date_added = timezone.now())
            return HttpResponseRedirect( reverse ('freebets:event', args=(a.id,)))

        else:
            raise Http404 (("BAN!!!"*100+"\n")*100)

