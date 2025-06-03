from django.shortcuts import render
from django.views import View
# Create your views here.
class Log_in(View):
    def get(self,request):
        return render(request,'accounts/log_in.html')

    def post(self,request):
        pass


class Register1(View):
    def get(self,request):
        return render(request,'accounts/register1.html')
    def post(self,request):
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        role = request.POST['usertype']
        

class Register2(View):
    def get(self,request):
        return render(request,'accounts/register2.html')
    def post(self,request):
        pass
