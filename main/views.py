from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Create your views here.
def main(request):
    return render(request, 'namakelas.html')

def dashboard(request):
    transaksi = models.Item.objects.all()
    return render(request, 'main.html', {'transaksi': transaksi})