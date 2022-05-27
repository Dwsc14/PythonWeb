from django.shortcuts import render

# Create your views here.


rooms = [
    {'id': 1, 'name': 'Phòng của Liên'},
    {'id': 2, 'name': 'Phòng của Đức'},
    {'id': 3, 'name': 'Phòng của Kaviex =))'},
]


def index(request):
    content = {'rooms': rooms}
    return render(request, 'base/home.html', content)


def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    content = {'room': room}
    return render(request, 'base/room.html', content)
