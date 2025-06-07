from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
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

def request_room_view(request):
    try:
        if request.method == 'POST':
            fname = request.POST['fullname']
            phone = request.POST['phone']        
            email = request.POST['email']        
            message = request.POST['message']        
            area = request.POST['area']        
            propertytype = request.POST['propertytype']        
            location = request.POST['location'] 
            data = RequestRoom(fullname=fname,phone=phone,email=email,message=message,property_type=propertytype,area=area,location=location)
            data.full_clean()
            data.save()
            messages.success(request,'form submitted successfully!')
            return redirect('request_room')

    except Exception as e:
        messages.error(request,f'{str(e)}')
        return redirect('request_room')       
    return render(request,'UI/request.html')


def shifthome(request):
    if request.method == 'POST':
            fname = request.POST['fullname']
            phone = request.POST['phone']        
            email = request.POST['email']        
            message = request.POST['message']        
            area = request.POST['area']        
            propertytype = request.POST['propertytype']        
            current_location = request.POST['current_location'] 
            location2 = request.POST['location']
            date = request.POST['date']
            data = ShiftHome(fullname=fname,phone=phone,email=email,message=message,property1 =propertytype,area=area,location1=current_location, location2 = location2,date=date)
            data.full_clean()
            data.save()
            messages.success(request,'form submitted successfully!')
            return redirect('shifthome')
    return render(request,'UI/shifthome.html')


def aboutus(request):
    return render(request,'UI/aboutus.html')


def addproperty(request):
    if request.method == 'POST':
        title = request.POST['title']
        address = request.POST['location']
        propertytype = request.POST['propertytype']
        price = request.POST['price']
        message = request.POST['message']
        tole = request.POST['area']
        data = property_post(title=title,address = address, property_type = propertytype,price= price, extra_info = message,area = tole)
        data.full_clean()
        data.save()
        messages.success(request,'Property addedsuccessfully!')
        return redirect('shifthome')
    return render(request,'UI/property_post.html')