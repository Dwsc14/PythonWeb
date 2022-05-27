from django.shortcuts import render
from .models import Room

# Create your views here.


def index(request):
    rooms = Room.objects.all()
    content = {'rooms': rooms}
    return render(request, 'base/home.html', content)


def room(request, pk):
    room = Room.objects.get(id=pk)
    content = {'room': room}
    return render(request, 'base/room.html', content)
