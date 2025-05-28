from django.shortcuts import render
from django.views import View
# Create your views here.
class Log_in(View):
    def get(self,request):
        return render(request,'accounts/log_in.html')

    def post(self,request):
        pass


class Register(View):
    def get(self,request):
        return render(request,'accounts/register.html')
    def post(self,request):
        pass
       
        
