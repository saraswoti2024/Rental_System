from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
from accounts.models import CustomUser


def one_hour_later():
    return timezone.now().time()

def current_date():
    return timezone.now().date()

class Choice1(models.Model):
    choice = models.CharField(max_length=60)

    def __str__(self):
        return self.choice

FACILITY_CHOICES = [
    ('GYM', 'GYM'),
    ('School', 'School'),
    ('Swimming Pool', 'Swimming Pool'),
    ('Hospital', 'Hospital'),
    ('Banquet Hall', 'Banquet Hall'),
    ('College', 'College')
]
class property_post(models.Model):
    title = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    property_type = models.CharField(max_length=100,null=True)
    area = models.CharField(max_length=100,null=True)
    main_photo = models.ImageField(blank=False)
    photo1 = models.ImageField(blank=False,upload_to="property_images")
    photo2 = models.ImageField(blank=False,upload_to="property_images")
    photo3 = models.ImageField(blank=True,upload_to="property_images")
    photo4 = models.ImageField(blank=True,upload_to="property_images")
    facilities = MultiSelectField(choices=FACILITY_CHOICES,null=True)
    video = models.FileField(upload_to="property_video",blank=True,null=True)
    phone = PhoneNumberField(region='NP')
    price = models.IntegerField()
    extra_info = models.TextField()
    is_approved = models.BooleanField(default=False)
    date = models.DateField(default=current_date)
    time = models.TimeField(default=one_hour_later)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_reports = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class RequestRoom(models.Model):
    fullname = models.CharField(max_length=100)
    phone = PhoneNumberField(region='NP')
    email = models.EmailField()
    location = models.CharField(max_length=200)
    property_type = models.CharField(max_length=200)
    message = models.TextField()
    area = models.CharField(max_length=100)



class ShiftHome(models.Model):
    BOOKING_CHOICES = [
    ('instant', 'Instant Booking'),
    ('schedule', 'Schedule For Later'),
    ]
    booking_type = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='instant')
    phone = PhoneNumberField(region='NP')
    email = models.EmailField()
    location1 = models.CharField(max_length=200)
    location2 = models.CharField(max_length=200)
    property1 = models.CharField(max_length=200)
    message = models.TextField()
    cupboard = models.IntegerField(default=0)
    bed = models.IntegerField(default=0)
    tv = models.IntegerField(default=0)
    table = models.IntegerField(default=0)
    sofa = models.IntegerField(default=0)
    time = models.TimeField(default=one_hour_later) 
    date = models.DateField(default=current_date)    
    def clean(self):
        super().clean()
        if self.date:
            if self.date < timezone.now().date():
                raise ValidationError({'date': "Date cannot be in the past."})

class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Fraud_Reports(models.Model):
    property_name = models.ForeignKey(property_post,on_delete=models.CASCADE,null=True)
    message = models.TextField()
    reporter_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    is_report = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)  # when the report was made
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_img")
    
class Inquiry(models.Model):
    property = models.ForeignKey(property_post, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_inquiries')  # RentSeeker
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Inquiry from {self.sender.username} to {self.property.user.username}'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    
class Testimonals(models.Model):
        name = models.CharField(max_length=100)
        comment = models.TextField()
        user_type = models.CharField(max_length=100,null=True)
        image = models.ImageField(upload_to="testimonals",null=True)

class comment_post(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    property = models.ForeignKey(property_post,on_delete=models.CASCADE)
    comment = models.TextField()