from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import User
class UserProfile(models.Model):
    u = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='webapp/prof_pic',blank=True)
    phone_no = models.CharField(max_length=10)
    def __str__(self):
        return self.u.username
class room_type(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=10)
    cost = models.PositiveIntegerField()
    def __str__(self):
        return self.type
class addons(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    f_type = models.ForeignKey(room_type,on_delete = models.CASCADE)
    addon = models.CharField(max_length=20)
    pre_book = models.BooleanField()

    def __str__(self):
        return self.type

class rooms(models.Model):
    image = models.ImageField(upload_to='webapp/room_pics')
    room_no = models.CharField(max_length = 5,primary_key=True)
    type = models.ForeignKey(room_type,on_delete = models.CASCADE)
    description = models.CharField(max_length=20000)
    occupied = models.BooleanField()

    def __str__(self):
        return self.room_no
class reservations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    u_id = models.ForeignKey(User,on_delete=models.CASCADE)
    r_id = models.ForeignKey(rooms,on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=15)
    def __str__(self):
        return str(self.id)
