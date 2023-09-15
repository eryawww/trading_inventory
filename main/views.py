from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from . import models

from main.forms import ItemForm
from main.models import Item

# Create your views here.
def main(request: HttpRequest):
    if request.method == 'POST':
        pass
    data = models.Item.objects.all()
    len_data = len(data)
    adddata_url = '/create'
    return render(request, 'main.html', dict(data=data, adddata_url=adddata_url, len_data=len_data))

def create(request: HttpRequest):
    print(request.POST)
    form = ItemForm(request.POST or None)

    if request.method == 'POST':
        form.save()
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
    print(data)
    return HttpResponse(serializers.serialize('xml', data), content_type='application/xml')

def show_jsonbyid(request, id: int):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')
