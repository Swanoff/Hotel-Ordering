from django import forms
from webapp.models import UserProfile
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=('username','password','email')

class RegForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('profile_pic','phone_no')
