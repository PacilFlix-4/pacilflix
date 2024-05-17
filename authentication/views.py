from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

# Create your views here.
def get_pengguna(request):
    try:
        return request.session["pengguna"]
    except KeyError:
        return None

def show_landing(request):
    if get_pengguna(request) != None:
        return redirect(reverse("show:show_main"))
    
    return render(request, 'main.html', context={})

def user_login(request):
    if get_pengguna(request) != None:
        return HttpResponseRedirect(reverse("authentication:landing_page"))
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        raw_query = "SELECT * FROM PENGGUNA WHERE username='{username}' AND password='{password}'"
        query = raw_query.format(username=username, password=password)

        cursor = connection.cursor()
        cursor.execute(query)
        query_output = cursor.fetchall()
        cursor.close()

        if len(query_output) == 1:
            request.session["pengguna"] = username
            return redirect(reverse("authentication:landing_page"))
        else:
            messages.info(request, 'Incorrect username or password')

    context = {'page_title': "Login"}
    return render(request, 'login.html', context)

def user_register(request):
    if get_pengguna(request) != None:
        return HttpResponseRedirect(reverse("authentication:landing_page"))
    
    if request.method == "POST" and request.POST.get('password1') == request.POST.get('password2'):
        username = request.POST.get('username')
        password = request.POST.get('password1')
        country = request.POST.get('country')

        raw_query = "INSERT INTO PENGGUNA VALUES ('{username}', '{password}', '{country}')"
        query = raw_query.format(username=username, password=password, country=country)

        cursor = connection.cursor()
        try:
            cursor.execute(query)
            request.session["pengguna"] = username
            response = HttpResponseRedirect(reverse("show:show_main"))
            return response
        except:
            messages.info(request, 'Username already exists!')
        finally:
            cursor.close()
    context = {'page_title': "Register"}
    return render(request, 'register.html', context)

def user_logout(request):
    request.session["pengguna"] = None
    response = HttpResponseRedirect(reverse('authentication:landing_page'))
    return response