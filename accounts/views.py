from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
# from django.contrib.auth.models import CustomUserModel
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import re
from UI.views import HomeView
# Create your views here.
class Log_in(View):
    def get(self,request):
        return render(request,'accounts/log_in.html')

    def post(self,request):
        try: 
            uname = request.POST['username']
            password = request.POST['password']
            if not CustomUser.objects.filter(username=uname).exists():
                messages.error(request,'username doesnot exists!')
                return redirect('log_in')
            else:
                value = authenticate(username=uname,password=password)
                if value is not None:
                    login(request,value)
                    if value.is_superuser or value.is_staff:
                        return redirect('/admin/')
                    elif value.usertype == 'landlord':
                        return redirect('landlord_home')
                    elif value.usertype == 'rentseeker':
                        return redirect('home')
                   
                else:
                    messages.error(request,'password is not valid!')
                    return redirect('log_in')
        except Exception as e:
            messages.error(request,f'{str(e)}')
            return redirect('log_in')
class Register1(View):
    def get(self,request):
        return render(request,'accounts/register1.html')
    def post(self,request):
        try: 
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password1 = request.POST['password1']
            role = request.POST['usertype']
            if password == password1:
                validate_password(password)
                if password == username:
                    messages.error(request,'password and uname shouldn\'t be same')
                    return redirect('register1')
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request,'email already exists!')
                    return redirect('register1')
                if CustomUser.objects.filter(username=username).exists():
                    messages.error(request,'username already exists!')
                    return redirect('register1')
                CustomUser.objects.create_user(first_name = fname,last_name = lname, username=username,email=email , password = password,usertype=role)
                messages.success(request,'successfully created!')
                return redirect('register1')
        except Exception as e:
            messages.error(request,f'{str(e)}')
            return redirect('register1')

def log_out(request):
    logout(request)
    return redirect('log_in')
        
