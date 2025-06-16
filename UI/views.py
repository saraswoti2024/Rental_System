from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import *
from django.contrib import messages
from .decorators import *
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
# Create your views here.


def is_valid_image(file):
    return file.content_type.startswith('image/')

def is_valid_video(file):
    return file.content_type.startswith('video/')

class HomeView(View):
    def post(self,request):
        pass
    def get(self,request): 
        data = property_post.objects.filter(is_approved=True).order_by('-date')[:5]
        context = {
            'feature' : data,
        }
        return render(request,'UI/home.html',context)

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
    try:
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
                email1 = email[:6]
            
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
                  ##gmail starts
                subject = "Home Shifting"
                message = render_to_string('UI/gmail2.html',{'name': email1 ,'date':datetime.now(),'date1': date,'time': time})
                from_email = 'saraswotikhadka2k2@gmail.com'
                recipient_list = [email]
                emailmsg = EmailMessage(subject,message,from_email,recipient_list)
                emailmsg.send(fail_silently=True)
                ##gmail ends
                messages.success(request,'form submitted successfully!')
                return redirect('shifthome')
    except Exception as e:
        messages.error(request,f'{str(e)}')
        return redirect('shifthome')
    return render(request,'UI/shifthome.html')


def aboutus(request):
    return render(request,'UI/aboutus.html')


@landlord_required
def addproperty(request):
    if request.method == 'POST' and request.FILES:
        title = request.POST['title']
        address = request.POST['location']
        propertytype = request.POST['propertytype']
        phone = request.POST['phone']
        facilities = request.POST.getlist('facilities[]')
        price = request.POST['price']
        video = request.FILES.get('video')
        mainphoto = request.FILES.get('main_photo')
        photo1 = request.FILES.get('photo1')
        photo2 = request.FILES.get('photo2')
        photo3 = request.FILES.get('photo3')
        photo4 = request.FILES.get('photo4')
        message = request.POST['message']
        tole = request.POST['area']

        if mainphoto and not is_valid_image(mainphoto):
            messages.error(request,'must be image')
        if photo1 and not is_valid_image(photo1):
            messages.error(request,'must be image')
        if photo2 and not is_valid_image(photo2):
            messages.error(request,'must be image')
        if photo3 and not is_valid_image(photo3):
            messages.error(request,'must be image')
        if photo4 and not is_valid_image(photo4):
            messages.error(request,'must be image')

        if video and not is_valid_video(video):
            messages.error(request,'must be video')

        data = property_post(title=title,address = address, property_type = propertytype,price= price, extra_info = message,area = tole,video=video,main_photo = mainphoto,photo1=photo1,photo2=photo2,photo3=photo3,photo4=photo4,facilities=facilities,phone=phone)
        data.full_clean()
        data.save()
        messages.success(request,'Property added successfully!')
        return redirect('addproperty')
    return render(request,'UI/property_post.html')

@landlord_required
def landlord_home(request):
    return render(request,'UI/home_landlord.html')

@landlord_required
def landlord_dashboard(request):
    data = property_post.objects.all()
    context = {
        'property' : data,
    }
    return render(request,'UI/Ldashboard.html',context)

def delete_property(request,id):
     data = get_object_or_404(property_post, id=id) 
     data.delete()
     return redirect('ldashboard')

def house(request):
    
    data = property_post.objects.filter(property_type="House",is_approved=True).order_by('-date')
    context = {
        'houses' : data
    }
    return render(request,'UI/house.html',context)

def flat(request):
    
    data = property_post.objects.filter(property_type="Flat",is_approved=True).order_by('-date')
    context = {
        'flat' : data
    }
    return render(request,'UI/Flat.html',context)

def officespace(request):
    
    data = property_post.objects.filter(property_type="office_space",is_approved=True).order_by('-date')
    context = {
        'office' : data
    }
    return render(request,'UI/office.html',context)

def land(request):
    data = property_post.objects.filter(property_type="lands",is_approved=True).order_by('-date')
    context = {
        'land' : data
    }
    return render(request,'UI/land.html',context)

def shutter(request):
    
    data = property_post.objects.filter(property_type="shutters",is_approved=True).order_by('-date')
    context = {
        'shutter' : data
    }
    return render(request,'UI/shutter.html',context)

def Room(request):
    
    data = property_post.objects.filter(property_type="Room",is_approved=True).order_by('-date')
    context = {
        'room' : data
    }
    return render(request,'UI/Room.html',context)
