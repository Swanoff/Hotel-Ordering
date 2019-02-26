from django.shortcuts import render,redirect
from webapp.forms import LoginForm
from webapp.forms import RegForm
from django.contrib.auth.models import User
from webapp.models import UserProfile
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.
def index(request):
    print(request.user.is_authenticated)
    if(request.user.is_authenticated):
        return redirect('home')
    form1 = LoginForm()
    form2  = RegForm()
    form = {"form1":form1,"form2":form2}
    return render(request,'webapp/login.html',context = form)
def contact(request):
    return render(request,'webapp/test.html')
def register(request):
    registered = False
    form1 = LoginForm(request.POST)
    form2 = RegForm(request.POST)
    form = {"form1":form1,"form2":form2}
    form['registered'] = registered
    if form1.is_valid() and form2.is_valid():
        user = form1.save(commit=False)

        user.set_password(user.password)
        user.save()
        prof = form2.save(commit=False)
        prof.u = user
        prof.save()
        registered = True
        form['registered'] = registered
        return render(request,'webapp/login.html',context = form)
    else:
        return render(request,'webapp/login.html',context = form)


def user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(password)
    # print(request.POST)  <h2>Homepage</h2>
    user = authenticate(username = username,password = password)
    if user:
        login(request,user)
        return redirect('home')
    else:
        return render(request,'webapp/login.html',context={'errors':"Wrong Username or password"})
@login_required(login_url='/')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
@login_required(login_url='/')
def home(request):
    return render(request, 'webapp/home.html')
@login_required(login_url='/')
def settings(request):
    user = request.user
    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'webapp/settings.html', {
        'google_login' : google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })
@login_required(login_url = '/')
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'webapp/password.html', {'form': form})
