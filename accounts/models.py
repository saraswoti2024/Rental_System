from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    user_type = (
        ('landlord', 'Landlord'),
        ('rentseeker', 'Rentseeker'),
    )

    usertype = models.CharField(max_length=100,choices=user_type,default="rentseeker")
