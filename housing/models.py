from django.db import models
from django.contrib.auth.models import User

# Create your models here.

GENDER = (
    ('M', 'Male'),# first one is for backend while the other one is for the frontend
    ('F', 'Female'),
)
class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        phone = models.CharField(max_length=50)
        fullname = models.CharField(max_length=255)
        gender = models.CharField(max_length=10, choices=GENDER)
        profile_pix = models.ImageField(upload_to='profile', blank=True, null=True)#pip install pillow to allow for image to be uploaded
        
        def __str__(self):
            return self.fullname
 