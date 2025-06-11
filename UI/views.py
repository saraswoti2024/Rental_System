from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib import messages
from .decorators import *
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
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
             ##gmail starts
            subject = "Room Request"
            message = render_to_string('UI/gmail.html',{'name': fname ,'date':datetime.now()})
            from_email = 'saraswotikhadka2k2@gmail.com'
            recipient_list = [email]
            emailmsg = EmailMessage(subject,message,from_email,recipient_list)
            emailmsg.send(fail_silently=True)
            ##gmail ends
            messages.success(request,f" your form submitted successfully")
            return redirect('request_room')

    except Exception as e:
        messages.error(request,f'{str(e)}')
        return redirect('request_room')       
    return render(request,'UI/request.html')


def shifthome(request):
    if request.method == 'POST':
            phone = request.POST['phone']        
            email = request.POST['email']        
            message = request.POST['message']              
            propertytype = request.POST['type']        
            current_location = request.POST['location1'] 
            location2 = request.POST['location2']
            bed = request.POST['bed']
            sofa = request.POST['sofa']
            cupboard= request.POST['cupboard']
            tv = request.POST['tv']
            table = request.POST['table']
          
            booking_type = request.POST['booking_type']
            if booking_type == 'instant':
                  date = timezone.now().date()  
                  time = timezone.now().time().replace(microsecond=0)
            else:
                time = request.POST['time']
                date = request.POST['date']
            data = ShiftHome(phone=phone,email=email,message=message,property1 =propertytype,location1=current_location, location2 = location2,bed=bed,sofa=sofa,cupboard=cupboard,tv=tv,table=table,time=time,date=date,booking_type=booking_type)
            data.full_clean()
            data.save()
            messages.success(request,'form submitted successfully!')
            return redirect('shifthome')
    return render(request,'UI/shifthome.html')


def aboutus(request):
    return render(request,'UI/aboutus.html')


@landlord_required
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

@landlord_required
def landlord_home(request):
    return render(request,'UI/home_landlord.html')