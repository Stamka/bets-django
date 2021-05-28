from django.shortcuts import render
from .models import Event,Bet, User
from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from .forms import LoginForm
from django import forms
#import request
from .get_username import get_username
import requests 

##request = get_request()

def sample_view(request):
    current_user = request.user
    print (current_user.id)

def check_events():
    for a in Event.objects.all():
        #print(a.event_name)
        #print("status = ", a.event_result)
        cash1 = a.cash_to_first_team
        cash2 = a.cash_to_second_team
        user = User.objects.get(id=1)
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
        if a.event_result != 0:
            if a.event_result == 1:
                #print("xxx")
                a.cash_to_first_team += a.cash_to_second_team
                a.cash_to_second_team = 0
                a.save()
                for i in a.bet_set.all():
                    #print(i.eventBet)
                    if i.eventBet == "first":
                        #print("user cash now = ", user.cash)
                        if a.cash_to_first_team >= int(i.dollars * kef1):
                            user.cash += int(i.dollars * kef1)
                            #print("user cash now = ", user.cash)
                            user.save()
                            a.cash_to_first_team -= int(i.dollars * kef1)
                            a.save()
            if a.event_result == 2:
                a.cash_to_second_team += a.cash_to_first_team
                a.cash_to_first_team = 0
                a.save()
                for i in a.bet_set.all():
                    if i.eventBet == "second":
                        if a.cash_to_second_team >= int(i.dollars * kef2):
                            user.cash += int(i.dollars * kef2)
                            user.save()
                            a.cash_to_second_team -= int(i.dollars * kef2)
                            a.save()
            a.cash_to_first_team = 0
            a.cash_to_second_team = 0
            a.bet_set.all().delete()
            a.event_result = 0
            a.save()


def index(request):
    check_events()
    new_bets_list = Event.objects.all().filter().order_by('-event_date')
    user = User.objects.get(id=1)
    
    return render(request, 'bets.html',{'new_bets':new_bets_list, 'user':user})

def no_money(request):
    return render(request, 'no_money.html')

def event(request, event_id, alert=0):
    current_user = request.user
    print ('=====', current_user.id)
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
    check_events()
    if Event.
    return render(request, 'event.html', {'event': a, 'latest_bets' : latest_bets, 'user': user,
                                          'k1': kef1,'k2': kef2,'cash1':cash1,'cash2': cash2 })

def feel_cash(request):
    check_events()
    b = User.objects.get(id=currentUserId())
    dollars = request.POST['feel_money']
    if int(dollars) >= 0:
        b.cash +=int( dollars)
        b.save()
        return HttpResponseRedirect(reverse('freebets:index'))
    else:
        raise Http404(("BAN!!!" * 100 + "\n") * 100)

def make_bet(request, event_id):
    check_events()
    try:
        a=Event.objects.get( id = event_id)

    except:
        raise Http404("Такого матча нет")

    b = User.objects.get(id=currentUserId())
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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})