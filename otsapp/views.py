import json
import pytz
import collections, calendar
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Sum,Count
from django.db import connection

from otsapp.models import UserProfile, Transaction,\
    Client, Trader, Oil, Rating



@login_required
def index(request):
    return HttpResponse("Test index...")


def login(request):
    if request.method == "GET":
        return render(request, 'otsapp/loginview.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,
            password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            return HttpResponse(json.dumps({"success":True}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"success":False}),
                                content_type="application/json")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/ots/")

def get_local_tz(tn):
    local_tz = pytz.timezone('US/Central')
    tn.date = tn.date.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return tz

def home_dashborad(request):
    if request.method == "GET":
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        if user_prof.user_type == 0:
            client = Client.objects.get(user_profile=user_prof)
            oil_rate = (Oil.objects.all()[0]).current_unit_price
            #transactions = map(get_local_tz,Transaction.objects.filter(client__user_profile__user=user))
            transactions = Transaction.objects.filter(client__user_profile__user=user)
            import random
            trader = random.choice(Trader.objects.all())
            context = {
                        "money":client.money, "oil":client.oil, "firstname":user.first_name, 
                        "pending_transactions":[tn for tn in transactions if tn.status is 2],
                        "recent_transactions":[tn for tn in transactions if tn.status != 2],
                        "trader":trader, "current_oil_rate":oil_rate,
                        "commission_cash":client.rating.commission_rate_cash,
                        "commission_oil":client.rating.commission_rate_oil,
                        "traders":Trader.objects.all()
                    }
            _template = "otsapp/client_home.html"
        elif user_prof.user_type == 1:
            transactions = Transaction.objects.filter(trader__user_profile__user=user,
                    status=Transaction.STATUS_PENDING)
            context = {"firstname":user.first_name, "transactions":transactions}
            _template = "otsapp/trader_home.html"
        else:
            transactions = Transaction.objects.all()
            context = {"firstname":user.first_name, "transactions":transactions}
            _template = "otsapp/manager_home.html"

        return render(request, _template, context=context)

    elif request.method == "POST":
        user = request.user
        user_prof = UserProfile.objects.get(user=user)
        if user_prof.user_type == 2:
            data = json.loads(request.POST['data'])
            dateF = data['from_date']
            dateT = data['to_date']
            group_by = data['group_by']
            #dateF=datetime.datetime.strptime(request.POST['datef'], '%Y-%m-%d')
            #dateT=datetime.datetime.strptime(request.POST['datet'], '%Y-%m-%d')
            newDict=[]
            #while dateF.date() <datetime.datetime.now().date() and dateT.date() <= datetime.datetime.now().date():
            if group_by == 0:
                t=Transaction.objects.filter(date__range=(dateF,dateT)).extra({'date':"date(date)"}).values('date').annotate(created_count=Count('id'))
                for i in t:
                    newDict.append({"date": i.get('date'), "created_count":i.get("created_count")})
            elif group_by == 2:
                truncate_date = connection.ops.date_trunc_sql('month', 'date')
                qs = Transaction.objects.filter(date__range=(dateF,dateT)).extra({'month':truncate_date})
                report = qs.values('month').annotate(Count('pk')).order_by('month')
                for item in report:
                    month=calendar.month_name[int(str(item.get('month'))[5:7])]
                    num=item.get("pk__count")
                    newDict.append({'date':month,'created_count':num})
            else:
                t=Transaction.objects.filter(date__range=(dateF,dateT)).extra({'date':"date(date)"}).values('date').annotate(created_count=Count('id'))
                count=0
                startDate=datetime.strptime(dateF, "%Y-%m-%d")
                end=datetime.strptime(dateT, "%Y-%m-%d")
                tempdate=startDate-timedelta(days=1)
                weekCounter=0
                dict1={}
                for item in t:
                    date=str(item.get('date'))
                    num=item.get("created_count")
                    dict1[date]=num
                while tempdate<=end:
                    weeknum=0
                    for i in range(0,7):                    
                        tempdate=tempdate + timedelta(days=1)
                        actualDate=str(tempdate.year)+'-'+ str(tempdate.month) +'-'+ str(tempdate.day)
                        if (dict1.has_key(actualDate)):
                            weeknum += dict1[actualDate]
                    weekCounter+=1
                    newDict.append({'date':weekCounter,'created_count':weeknum})
        return HttpResponse(json.dumps({'newDict':newDict, 'view':group_by}), content_type="application/json")


def transaction(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.POST['data'])
        print data
        oil_rate = (Oil.objects.all()[0]).current_unit_price
        if data.get('t_id',None):
            try:
                #local_tz = pytz.timezone('US/Central')
                tn = Transaction.objects.get(id=data['t_id'])
                if data['action'] is 1:
                    client = tn.client
                    tn.status = Transaction.STATUS_APPROVED
                    tn.modified_datetime = timezone.now()
                    tn.save()
                    #current_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
                    #frm_time = current_utc.astimezone(local_tz)
                    #frm_time = datetime.combine(
                    #        datetime.date(frm_time.date().year,
                    #                      frm_time.date().month,
                    #                      1),
                    #                      datetime.min.time)
                    #frm_time = frm_time.astimezone(pytz.UTC)
                    cur_t = timezone.now()
                    print Transaction.objects.filter(client=client,
                            status=Transaction.STATUS_APPROVED,
                            date__year=cur_t.year,
                            date__month=cur_t.month).aggregate(
                            Sum('oil_barrel'))

                    if Transaction.objects.filter(client=client,
                            status=Transaction.STATUS_APPROVED,
                            date__year=cur_t.year,
                            date__month=cur_t.month).aggregate(
                            Sum('oil_barrel'))['oil_barrel__sum'] >= 30:

                        client.rating = Rating.objects.get(level=Rating.LEVEL_GOLD)
                        
                    if tn.tn_type is 0:
                        client.money -= tn.tn_cost
                    else:
                         client.money += tn.tn_cost

                    if tn.comm_type is 0:
                        client.money -= tn.comm_value
                    else:
                        client.oil -= tn.comm_value 

                    client.save()
                else:
                    tn.modified_datetime = timezone.now()
                    tn.status = Transaction.STATUS_CANCELED
                    tn.save()
            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({"success":False}),
                            content_type="application/json")
            else:    
                return HttpResponse(json.dumps({"success":True}),
                                content_type="application/json")

        client = Client.objects.get(user_profile__user=user)
        proceed=False
        if data['ttype'] is 0 and data['com_type'] is 0:
            if client.money > data['tn_cost'] + data['com_value']:
                proceed=True
        elif data['ttype'] is 0 and data['com_type'] is 1:
            if client.money >= data['tn_cost'] and client.oil >= data['com_value']:
                proceed=True
        elif data['ttype'] is 1 and data['com_type'] is 0:
            if client.oil >= data['oil_amount'] and client.money > data['com_value']:
                proceed=True
        elif data['ttype'] is 1 and data['com_type'] is 1:
            if client.oil >= data['oil_amount'] + data['com_value']:
                proceed=True

        if proceed:
            trader = Trader.objects.get(user_profile__user__id=data['trader'])
            Transaction.objects.create(client=client, trader=trader,
                tn_type=data['ttype'], oil_barrel=data['oil_amount'],
                tn_cost=data['tn_cost'], comm_type=data['com_type'],
                comm_value=data['com_value'], oil_unit_rate=oil_rate,
                status=Transaction.STATUS_PENDING)
            
            return HttpResponse(json.dumps({"success":True}),
                            content_type="application/json")
        else:
            return HttpResponse(json.dumps({"success":False}),
                            content_type="application/json")



def filter_transactions(request):
    if request.method == "POST":
        user = request.user
        trader = Trader.objects.get(user_profile__user=user)
        data = json.loads(request.POST['data'])
        from django.db.models import Q
        transactions = []
        if data['search_by'] == 0:
            transactions = Transaction.objects.filter(
                    Q(client__user_profile__user__first_name__istartswith=\
                    data['search_term'])|Q(
                    client__user_profile__user__first_name__iendswith=\
                    data['search_term'])|Q(
                    client__user_profile__user__last_name__istartswith=\
                    data['search_term'])|Q(
                    client__user_profile__user__last_name__iendswith=\
                    data['search_term']),
                    trader=trader, status__in=[Transaction.STATUS_APPROVED,\
                    Transaction.STATUS_CANCELED])

        elif data['search_by'] == 1:
            transactions = Transaction.objects.filter(
                    Q(client__location__street__icontains=\
                    data['search_term'])|Q(
                    client__location__zipcode__icontains=\
                    data['search_term'])|Q(
                    client__location__city__icontains=\
                    data['search_term'])|Q(
                    client__location__state__icontains=\
                    data['search_term']),
                    trader=trader, status__in=[Transaction.STATUS_APPROVED,\
                    Transaction.STATUS_CANCELED])
        
        transactions = map(lambda t: {
            "id": t.id,
            "date": t.date.strftime("%a, %b %d %Y, %I:%M %p"),
            "client_name": t.client.user_profile.user.first_name,
            "tn_type": t.tn_type,
            "tn_cost": str(t.tn_cost),
            "comm_type": t.comm_type,
            "comm_value": str(t.comm_value),
            "status": t.status,
            "oil_barrel": str(t.oil_barrel),
            "modified_datetime": t.modified_datetime.strftime(
                "%a, %b %d %Y, %I:%M %p")
        }, transactions)
        
        return HttpResponse(json.dumps({
            "firstname":user.first_name,
            "transactions":transactions,
            "search_term":data['search_term']
        }), content_type="application/json")