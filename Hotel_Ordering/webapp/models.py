from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    u = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='webapp/prof_pic',blank=True)
    phone_no = models.CharField(max_length=10)
    def __str__(self):
        return self.u.username
