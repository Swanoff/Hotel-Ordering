from django.db import models
# Create your models here.
from django.contrib.auth.models import User
class UserProfile(models.Model):
    u = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='webapp/prof_pic',blank=True)
    phone_no = models.CharField(max_length=10)
    def __str__(self):
        return self.u.username
