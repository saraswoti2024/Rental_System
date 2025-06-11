from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError


class Choice1(models.Model):
    choice = models.CharField(max_length=60)

    def __str__(self):
        return self.choice

class property_post(models.Model):
    title = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    property_type = models.CharField(max_length=100,null=True)
    area = models.CharField(max_length=100,null=True)
    price = models.IntegerField()
    extra_info = models.TextField()

    def __str__(self):
        return self.title

class RequestRoom(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    property_type = models.CharField(max_length=200)
    message = models.TextField()
    area = models.CharField(max_length=100)


def one_hour_later():
    return timezone.now().time()

def current_date():
    return timezone.now().date()

class ShiftHome(models.Model):
    BOOKING_CHOICES = [
    ('instant', 'Instant Booking'),
    ('schedule', 'Schedule For Later'),
    ]
    booking_type = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='instant')
    phone = models.IntegerField(null=True)
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