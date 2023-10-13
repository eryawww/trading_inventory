from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.core import serializers

from . import models
from main.forms import ItemForm
from main.models import Item
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import django.contrib.messages as messages

from django.views.decorators.csrf import csrf_exempt

def remove_data(request, pk):
    user_data = Item.objects.filter(user=request.user).filter(pk=pk).first()
    user_data.delete()

    return HttpResponse("Deleted", status_code=200)

def get_data(request, pk: str):
    # if pk = -1 then all
    pk = int(pk)
    if pk == -1:
        return HttpResponse(serializers.serialize('json', Item.objects.filter(user=request.user)), content_type='application/json')
    else:
        user_data = Item.objects.filter(user=request.user).filter(pk=pk)
        return HttpResponse(serializers.serialize('json', user_data), content_type='application/json')

@csrf_exempt
def edit_data(request, inc: str):
    inc = int(inc)
    pk = request.POST.get('pk')

    user_data = Item.objects.filter(user=request.user).filter(pk=pk).first()
    
    user_data.amount += inc
    user_data.save(update_fields=['amount'])
    data = {'data': user_data.amount}
    return JsonResponse(data)

@csrf_exempt
def add_product_ajax(request):
    user = request.user
    name = request.POST.get('name')
    buy_price = request.POST.get('price')
    amount = request.POST.get('amount')
    description = request.POST.get('description')
    time_buy = datetime.datetime.now()

    item = Item.objects.create(user=user, name=name, buy_price=buy_price, amount=amount, description=description, time_buy=time_buy)
    item.save()
    return HttpResponse("Saved")

def signup(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created!!!')
            return redirect('main:login')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:main')
        messages.warning(request, 'Incorrect Username or Password')
    context = {}
    return render(request, 'login.html', context)

def logout_page(request: HttpRequest):
    logout(request)
    response = redirect('main:login')
    response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return response

@login_required(login_url='/login')
def main(request: HttpRequest):
    if request.method == 'POST':
        pass
    data = models.Item.objects.filter(user=request.user)
    if data.count() == 0:
        last = []
        data = []
    else:
        last = data[data.count()-1]
        data = data[:data.count()-1]
    
    len_data = len(data)
    if len_data == 0:
        amount_data = 0
    else:
        amount_data = sum([x.amount for x in data])
    adddata_url = '/create'
    try:
        last_login = request.COOKIES['last_login']
    except KeyError:
        last_login = '-'
    try:
        ref = request.COOKIES['ref']
    except KeyError:
        ref = False

    context = dict(
        data=data,
        last=last,
        adddata_url=adddata_url,
        len_data=len_data,
        total_amount=amount_data,
        username = request.user.username,
        last_login = last_login,
        ref = ref
    )
    return render(request, 'main.html', context)

@login_required(login_url='/login')
def add_amount(request: HttpRequest, id: int):
    user_data = Item.objects.filter(user=request.user).filter(pk=id).first()
    user_data.amount += 1
    user_data.save(update_fields=['amount'])

    response = redirect('main:main')
    response.set_cookie('ref', f'Adding 1 Amount of {user_data.name} succeed!!!')
    return response

@login_required(login_url='/login')
def minus_amount(request: HttpRequest, id: int):
    user_data = Item.objects.filter(user=request.user).filter(pk=id).first()
    response = redirect('main:main')

    if user_data.amount == 0:
        response.set_cookie('ref', f'Failed, amount of {user_data.name} is 0!!!')
        return response

    user_data.amount -= 1
    user_data.save(update_fields=['amount'])

    response.set_cookie('ref', f'Removing 1 Amount of {user_data.name} succeed!!!')
    return response

@login_required(login_url='/login')
def delete(request: HttpRequest, id: int):
    user_data = Item.objects.filter(user=request.user).filter(pk=id).first()
    response = redirect('main:main')
    amount = user_data.amount
    name = user_data.name
    user_data.delete()
    response.set_cookie('ref', f'Removing {amount} Amount of {name} succeed!!!')
    return response

def create(request: HttpRequest):
    print(request.POST)
    form = ItemForm(request.POST or None)

    if request.method == 'POST':
        newdata = form.save(commit=False)
        newdata.user = request.user
        newdata.save()
        return HttpResponseRedirect(reverse('main:main'))
    return render(request, 'add.html', dict(form=form))

def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def show_xmlbyid(request, id: int):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_jsonbyid(request, id: int):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')