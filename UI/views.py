from django.shortcuts import render
from django.views import View

# Create your views here.
class HomeView(View):
    def post(self,request):
        pass
    def get(self,request):
        return render(request,'UI/home.html')
