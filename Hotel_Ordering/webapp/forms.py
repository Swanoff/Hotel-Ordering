from django import forms
from webapp.models import UserProfile
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=('username','password','email')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

class RegForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('profile_pic','phone_no')
