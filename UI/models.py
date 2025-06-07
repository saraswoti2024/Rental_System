from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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


class ShiftHome(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.IntegerField(null=True)
    email = models.EmailField()
    location1 = models.CharField(max_length=200)
    location2 = models.CharField(max_length=200)
    property1 = models.CharField(max_length=200)
    message = models.TextField()
    area = models.CharField(max_length=100)
    date = models.DateField()