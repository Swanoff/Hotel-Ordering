from django.shortcuts import render,redirect
from django.urls import reverse
from webapp.forms import LoginForm
from webapp.forms import RegForm
from django.contrib.auth.models import User
from webapp.models import UserProfile,reservations,rooms,addons,room_type
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import date
# Create your views here.
def index(request):
    print(request.user.is_authenticated)
    if(request.user.is_authenticated):
        return redirect('home')
    form1 = LoginForm()
    form2  = RegForm()
    form = {"form1":form1,"form2":form2}
    return render(request,'webapp/login.html',context = form)
def about(request):
    return render(request,'webapp/about_us.html')
def contact(request):
    return render(request,'webapp/contact_us.html')
def room(request):
    return render(request,'webapp/rooms.html')
def gallery(request):
    return render(request,'webapp/boo.html')
def awards(request):
    return render(request,'webapp/awards.html')
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
@login_required
@csrf_exempt
def results(request):
    if(request.method=="POST"):
        data = request.POST
        req_r = reservations.objects.all()
        req_a = []
        check_i,check_o = data['check_in'],data['check_out']
        check_i = date(*map(int, check_i.split('-')))
        check_o = date(*map(int, check_o.split('-')))
        s = []
        for i in req_r:
            a = (i.check_in,i.check_out)
            b = (check_i,check_o)
            if(a[0]>=b[0]):
                if(b[1]>=a[0]):
                    s.append(i.r_id)
            else:
                if(b[0]<=a[1]):
                    s.append(i.r_id)
        # print(s)
        all_r = rooms.objects.all()
        obj = []
        for i in all_r:
            if(i not in s):
                obj.append(i)
        # print(obj)
        return render(request, 'webapp/results.html',context={'obj':obj,'check_in':data['check_in'],'check_out':data['check_out']})

@login_required(login_url='/')
@csrf_exempt
def reserve(request):
    data = request.POST
    user = request.user
    r_id = data['id']
    check_in = date(*map(int, data['check_in'].split('-')))
    check_out = date(*map(int, data['check_out'].split('-')))
    r = rooms.objects.get(room_no = r_id)
    res = reservations(u_id = user,r_id = r,check_in=check_in,check_out=check_out,status=False)
    res.save()
    return HttpResponseRedirect('/settings/')
@login_required(login_url='/')
@csrf_exempt
def cancel(request):
    data = request.POST
    id = data['id']
    res = reservations.objects.get(id = id)
    res.delete()
    return HttpResponseRedirect('/settings/')
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
    n_reservation = reservations.objects.filter(u_id=request.user)
    r = []
    c = []
    for i in n_reservation:
        temp = rooms.objects.get(room_no = i.r_id)
        r.append(rooms.objects.get(room_no = i.r_id))
        c.append(room_type.objects.get(type=temp.type))
    data  = zip(n_reservation,r,c)
    return render(request, 'webapp/settings.html', {
        'google_login' : google_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect,
        'data':data,
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
