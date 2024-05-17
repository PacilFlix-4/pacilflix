from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from authentication.models import Pengguna

from .forms import PenggunaCreationForm

# Create your views here.
def show_landing(request):
    if request.user.is_authenticated:
        return redirect(reverse("show:tayangan"))
    
    return render(request, 'main.html', context={})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authentication:landing_page"))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("authentication:landing_page"))
        else:
            messages.info(request, 'Incorrect username or password')

    context = {'page_title': "Login"}
    return render(request, 'login.html', context)

def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("authentication:landing_page"))
    
    form = PenggunaCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_user = form.save()

            # buat objek pengguna juga
            pengguna = Pengguna()
            pengguna.user = new_user
            pengguna.country = form.cleaned_data['country']
            pengguna.save()

            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            response = HttpResponseRedirect(reverse("show:show_main"))
            return response
    context = {'page_title': "Register", 'form': form}
    return render(request, 'register.html', context)

def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:landing_page'))
    return response