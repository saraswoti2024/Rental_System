from django.db import models
from phonenumber_field.formfields import PhoneNumberField


class Choice1(models.Model):
    choice = models.CharField(max_length=60)

    def __str__(self):
        return self.choice

class Featured(models.Model):
    title = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    property_type = models.ForeignKey(Choice1,on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.title

class RequestRoom(models.Model):
    fullname = models.CharField(max_length=100)
    phone = PhoneNumberField()
    email = models.EmailField()
    location = models.CharField(max_length=200)
    property = models.CharField(max_length=200)
    message = models.TextField()
    area = models.CharField(max_length=100)

