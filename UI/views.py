from django.shortcuts import render
from django.views import View
from .models import *
# Create your views here.
class HomeView(View):
    def post(self,request):
        pass
    def get(self,request):
        return render(request,'UI/home.html')

def choices(request):
    return render(request,'UI/choices.html')

def common(request):
    data = Choice1.objects.all()
    return render(request,'UI/common.html',{'nav': data})