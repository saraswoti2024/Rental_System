from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import *
from django.contrib import messages
from .decorators import *
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
import os
import json
from django.conf import settings
# Create your views here.
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required


def is_valid_image(file):
    return file.content_type.startswith('image/')

def is_valid_video(file):
    return file.content_type.startswith('video/')

class HomeView(View):
    def post(self,request):
        pass
    def get(self,request): 
        file_path = os.path.join(settings.BASE_DIR, 'UI/static/data/nepal_places.json')
        f = open(file_path, 'r', encoding='utf-8') 
        data_loc = json.load(f)
        places = [f"{item['name']}, {item['city']}" for item in data_loc]
        feature = property_post.objects.filter(is_approved=True).order_by('-date')[:5]
        searched = False
        data = None
        title = request.GET.get('title')
        price = request.GET.get('price')
        propertytype = request.GET.get('propertytype')
        location = request.GET.get('location')
        
        if title or price or propertytype or location:
            data = property_post.objects.filter(is_approved=True)
            searched = True
            
            if title:
                data = data.filter(title__icontains=title)
            else:
                data = property_post.objects.filter(is_approved=True)
            
            if price :
                try:
                        min_price, max_price = map(int, price.replace(" ", "").split('-'))
                        data = data.filter(price__gte=min_price, price__lte=max_price)
                except:
                        pass  # Don't crash if input is bad
            else:
                data = property_post.objects.filter(is_approved=True)
            
            if propertytype :
                data = data.filter(property_type__iexact=propertytype) 
            else:
                data = property_post.objects.filter(is_approved=True)
            
            if location :
                data = data.filter(address__icontains=location) 
            else:
                data = property_post.objects.filter(is_approved=True) 
            
        context = {
            'data' : data,
            'feature' : feature,
            'searched' : searched,
           	'places' : places, 
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
            ActivityLog.objects.create(
                user= request.user if request.user.is_authenticated else None,
                action = f"Request for Room added ({data.property_type})"
                )
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
                ActivityLog.objects.create( user=request.user if request.user.is_authenticated else None,action =f'shift home request added ({data.booking_type})')
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
    file_path = os.path.join(settings.BASE_DIR, 'UI/static/data/nepal_places.json')
    f = open(file_path, 'r', encoding='utf-8') 
    data = json.load(f)
    places = [f"{item['name']}, {item['city']}" for item in data]
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

        data = property_post(title=title,address = address, property_type = propertytype,price= price, extra_info = message,area = tole,video=video,main_photo = mainphoto,photo1=photo1,photo2=photo2,photo3=photo3,photo4=photo4,facilities=facilities,phone=phone,user=request.user)
        data.full_clean()
        data.save()
        ActivityLog.objects.create(user=request.user,action =f'Added property ({data.title})')
        messages.success(request,'Property added successfully!')
        return redirect('addproperty')
    return render(request,'UI/property_post.html',{'places':places})

@landlord_required
def landlord_home(request):
    return render(request,'UI/home_landlord.html')

@landlord_required
def landlord_dashboard(request):
    data = property_post.objects.filter(user = request.user)
    pending_ads = property_post.objects.filter(is_approved=False,user = request.user)
    approved_ads = property_post.objects.filter(is_approved=True,user = request.user)

    context = {
        'pending_ads': pending_ads,
        'approved_ads': approved_ads,
        'property' : data,
        
    }
    return render(request,'UI/Ldashboard.html',context)

def delete_property(request,id):
     data = get_object_or_404(property_post, id=id) 
     data.delete()

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

def edit_ldashboard(request,id):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'UI/static/data/nepal_places.json')
        f = open(file_path, 'r', encoding='utf-8') 
        data = json.load(f)
        places = [f"{item['name']}, {item['city']}" for item in data]
        data = property_post.objects.get(id=id)
        if request.method == 'POST' and request.FILES:
            data = property_post.objects.get(id=id)
            if 'title' in request.POST:
                data.title = request.POST['title']
            if 'location' in request.POST:
                data.address = request.POST['location']
            if 'property_type' in request.POST:
                data.property_type = request.POST['property_type']
            if 'phone' in request.POST:
                data.phone = request.POST['phone']
            if 'facilities' in request.POST:
                data.facilities = request.POST.getlist('facilities')
            if 'price' in request.POST:
                data.price = request.POST['price']
            if 'video' in request.FILES:
                data.video = request.FILES.get('video')
            if 'main_photo' in request.FILES:
                data.main_photo = request.FILES.get('main_photo')
            if 'photo1' in request.FILES:
                data.photo1 = request.FILES.get('photo1')
            if 'photo2' in request.FILES:
                data.photo2 = request.FILES.get('photo2')
            if 'photo3' in request.FILES:
                data.photo3 = request.FILES.get('photo3')
            if 'photo4' in request.FILES:
                data.photo4 = request.FILES.get('photo4')
            if 'extra_info' in request.POST:
                data.extra_info = request.POST['extra_info']
            if 'area' in request.FILES:
                data.area = request.POST['area']
            if 'mainphoto' in request.FILES and not is_valid_image('mainphoto'):
                messages.error(request,'must be image')
            if 'photo1' in request.FILES and not is_valid_image('photo1'):
                messages.error(request,'must be image')
            if 'photo2' in request.FILES and not is_valid_image('photo2'):
                messages.error(request,'must be image')
            if  'photo3' in request.FILES and not is_valid_image('photo3'):
                messages.error(request,'must be image')
            if 'photo4' in request.FILES and not is_valid_image('photo4'):
                messages.error(request,'must be image')

            if 'video' in request.FILES and not is_valid_image('video'):
                messages.error(request,'must be video')

            data.full_clean()
            data.save()
            ActivityLog.objects.create(user=request.user,action =f'edited property({data.title})')
            messages.success(request,'Property edited successfully!')
            return redirect('edit_ldashboard',data.id)
    except Exception as e:
        messages.error(request,f'{str(e)}')
        return redirect('edit_ldashboard',data.id)
    return render(request,'UI/edit.html',{'data':data,'places':places})

def property_detail(request,id):
    propertyy = property_post.objects.get(id=id)
    return render(request,'UI/property_detail.html',{'property' : propertyy})

@login_required(login_url='log_in')
def report(request,id):
    propertyy = get_object_or_404(property_post, id=id)  
    if request.method == 'POST':
        if Fraud_Reports.objects.filter(reporter_id=request.user,property_name=propertyy).exists():
            messages.error(request,'you have already submitted the report!')
            return redirect('report',id=propertyy.id)
        message = request.POST.get('reason')
        data = Fraud_Reports.objects.create(reporter_id=request.user,property_name=propertyy,message=message)
        data.full_clean()
        data.save()
        value = Fraud_Reports.objects.filter(property_name=propertyy).count()
        if value>4 and  not propertyy.is_reports :
            notify_admin_of_heavy_reports(propertyy, value)
            propertyy.is_reports= True
            propertyy.save()
        messages.success(request,'Reported Sucessfully!')
        return redirect('home')
    return render(request,'UI/report.html',{'property' : propertyy})

def notify_admin_of_heavy_reports(property_id,count):
    subject = f"🚨 ALERT: Property '{property_id.title}' reported {count} times!"
    message = f"""
    Attention Admin,

    The property titled "{property_id.title}" has received {count} reports.
    It may require review or action.
    Property ID: {property_id.id}
    View it in the admin panel or contact the user.

    Regards,
    Rental Safety System
    """
    from_email = 'saraswotikhadka2k2@gmail.com'
    recipient_list = ['optimistsaraswoti@gmail.com']
    emailmsg = EmailMessage(subject,message,from_email,recipient_list)
    emailmsg.send(fail_silently=False)
