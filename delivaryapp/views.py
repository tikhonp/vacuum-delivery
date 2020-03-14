from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from delivaryapp.models import userplaces, orders
from . import roboback
from threading import Thread
from time import time
from .config import Kitchen

def_places = roboback.def_places
terget_positions = roboback.terget_positions
robot = roboback.robocontrol()
# process = Thread(target=robot.main(), args=[])
# process.start()


def main(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/authed')
        return render(request, 'main.html')


def loginp(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/authed')
        else:
            return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            messages.error(request, 'Заполните все поля')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/authed')
        else:
            messages.error(request, 'Неправильный логин или пароль!')
            return redirect('/login')


def registerp(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/authed')
        else:
            return render(request, 'register.html')
    elif request.method == 'POST':
        name = request.POST.get('name', '')
        username = request.POST.get('login', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if username == '' or password1 == '' or password2 == '':
            messages.error(request, 'Не все поля заполнены')
            return redirect('/register')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ник уже занят')
            return redirect('/register')
        elif len(username) < 3:
            messages.error(request, 'Слишком короткий ник')
            return redirect('/register')
        elif len(username) > 20:
            messages.error(request, 'Слишком длинный ник')
            return redirect('/register')
        elif len(password1) < 6:
            messages.error(request, 'Слишком короткий пароль')
            return redirect('/register')
        elif len(password1) > 50:
            messages.error(request, 'Слишком длинный пароль')
            return redirect('/register')
        elif password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('/register')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1, first_name=name)
            user.save()
            login(request, user)
            return redirect('/authed')


def authedp(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            up = userplaces.objects.filter(author=request.user)
            if len(up) != 0 and up[0].is_active == True:
                return redirect('/authed/working/')
            else:
                Orders = orders.objects.filter(author=request.user)
                activeOrders = Orders.filter(is_closed=False)
                closedOrders = Orders.filter(is_closed=True)
                parms = {'username': request.user.username,
                         'user': request.user.first_name, 'activeOrders': activeOrders, 'closedOrders': closedOrders}
                return render(request, 'authed.html', parms)
    else:
        return redirect('/')


def logoutp(request):
    if request.method == 'GET':
        logout(request)
    return redirect('/')


def profilep(request):
    global def_places
    if request.user.is_authenticated:
        if request.method == 'GET':
            up = userplaces.objects.filter(author=request.user)
            if len(up) == 0:
                up = 0
            else:
                up = up[0].place
            parms = {'username': request.user.username, 'user': request.user.first_name,
                     "last_name": request.user.last_name, "email": request.user.email, "last_login": request.user.last_login, "up": up, 'def_places': def_places}
            return render(request, 'profile.html', parms)
        elif request.method == 'POST':
            if 'setplace' in request.POST:
                place = request.POST.get('place', '')
                if place == 0:
                    messages.error(request, 'Вы не выбрали комнату')
                else:
                    up = userplaces.objects.filter(author=request.user)
                    if len(up) == 0:
                        up = userplaces()
                        up.author = request.user
                        up.place = place
                        up.is_active = False
                        up.save()
                    else:
                        up = up[0]
                        up.place = place
                        up.save()
            elif 'pdatasubm' in request.POST:
                LastName = request.POST.get('LastName', '')
                FirstName = request.POST.get('FirstName', '')
                username = request.POST.get('username', '')
                email = request.POST.get('email', '')

                user = request.user
                user.first_name = FirstName
                user.last_name = LastName
                user.email = email
                user.username = username
                user.save()

            return redirect('/authed/profile/')
    else:
        return redirect('/')


def workingp(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            up = userplaces.objects.filter(author=request.user)
            if len(up) == 0:
                up = userplaces()
                up.author = request.user
                up.place = 0
                up.is_active = True
                up.place = Kitchen
                up.save()
            else:
                up = up[0]
                if not up.is_active:
                    if up.place == 0:
                        up.place = Kitchen
                    up.is_active = True
                    up.save()

            Orders = orders.objects.filter(is_closed=False)
            activeOrders = Orders.filter(is_active=False)
            workingOrders = Orders.filter(wuser=request.user.username)
            parms = {'username': request.user.username,
                     'user': request.user.first_name, 'activeOrders': activeOrders, 'workingOrders': workingOrders}
            return render(request, 'working.html', parms)
    else:
        return redirect('/')


def addorderp(request):
    global def_places
    if request.user.is_authenticated:
        if request.method == 'GET':
            up = userplaces.objects.filter(author=request.user)
            if len(up) == 0:
                up = 0
            else:
                up = up[0].place
            params = {'username': request.user.username,
                      'user': request.user.first_name, "up": up, 'def_places': def_places}
            return render(request, 'addorder.html', params)
        elif request.method == 'POST':
            place = request.POST.get('place', '')
            description = request.POST.get('description', '')

            order = orders()
            order.author = request.user
            order.place = place
            order.description = description
            order.save()
            return redirect('/authed')
    else:
        return redirect('/')


def stopworkingp(request):
    o = orders.objects.filter(is_active=True)
    for i in o:
        if o.wuser == request.user.username:
            o.wuser = 'None'
            o.is_active = False
    up = userplaces.objects.filter(author=request.user)
    up = up[0]
    up.is_active = False
    up.save()
    return redirect('/authed')


def getorderp(request):
    order_id = int(request.GET['order'])
    o = orders.objects.get(id=order_id)
    o.is_active = True
    o.wuser = request.user.username
    o.save()
    return redirect('/authed/working#workingo')


def compliteorderp(request):
    global terget_positions, def_places
    order_id = int(request.GET['order'])
    o = orders.objects.get(id=order_id)
    up = userplaces.objects.get(author=request.user)
    p = int(up.place)
    id = hash(time())
    x, y = terget_positions[p][0], terget_positions[p][1]
    print(x, y)
    robot.addtasks(x, y, id)
    out = robot.runtask(id)
    if not out == 'ok':
        print(out)
    placename = list(def_places.keys())[list(def_places.values()).index(p)]
    params = {'username': request.user.username,
              'user': request.user.first_name, 'o': o, 'placename': placename}
    return render(request, 'compliteorder.html', params)


def sendorderp(request):
    global terget_positions
    order_id = int(request.GET['order'])
    o = orders.objects.get(id=order_id)
    place = o.place
    id = hash(time())
    x, y = terget_positions[int(place)][0], terget_positions[int(place)][1]
    print(x, y)
    robot.addtasks(x, y, id)
    out = robot.runtask(id)
    if not out == 'ok':
        print(out)
    o.is_active = False
    o.is_closed = False
    o.save()
    return redirect('/authed/working/')


def cancelsendingp(request):
    robot.gohome()
    return redirect('/authed/working/')


def authgetorderp(request):
    order_id = int(request.GET['order'])
    o = orders.objects.get(id=order_id)
    robot.gohome()
    o.is_closed = True
    o.save()
    return redirect('/authed')


def testp(request):
    # o = orders.objects.get(id=3)
    out = str(robot.gettasks())
    return HttpResponse(out)
