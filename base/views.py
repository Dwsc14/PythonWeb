import django
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password do not right')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm
    context = {'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Your username or password were wrong!!')
    return render(request, 'base/login.html', context)


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__topic__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    # rooms = Room.objects.all()

    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__topic__icontains=q))
    content = {'rooms': rooms, 'topics': topics,
               'room_messages': room_messages}

    return render(request, 'base/home.html', content)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    practicipants = room.practicipants.all()

    context = {'room': room, 'messages': room_messages,
               'practicipants': practicipants}

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.practicipants.add(request.user)
        return redirect('room', pk=room.id)

    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    context = {'user': user, 'rooms': rooms}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def delete_comment(request, pk):
    message = Message.objects.get(id=pk)
    room = Room.objects.get(name=message.room)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room.id)

    return render(request, 'base/delete.html', {'obj': message})
