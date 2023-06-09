from django.shortcuts import render
from app.forms import *
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)

            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password')

    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)

        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()

            send_mail('Registration',
                      (f"Thanks For Registration MR.{NSUO.username} Your Registration is Succefully Done"),
                      'ganireddy8121@gmail.com',
                      [NSUO.email],
                      fail_silently=False
                      )
            return HttpResponse('REGISTRATION SUCCESSFULL')
        else:
            return HttpResponse('INVALID DATA')
        
    return render(request,'registration.html',d)

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

@login_required 
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password is changed successfully')
    return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        UN=request.POST['username']
        PW=request.POST['password']
        LUO=User.objects.filter(username=UN)
        print(LUO)
        if LUO:
            LUO[0].set_password(PW)
            LUO[0].save()
            return HttpResponse('Updated')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'forgot_password.html')    
   