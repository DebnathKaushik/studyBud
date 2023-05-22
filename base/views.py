from django.shortcuts import render ,redirect
from .models import Room
from .forms import RoomForm

# roomlist = [
#     {'id':1 , 'name':'Lets Learn Python'},
#     {'id':2 , 'name':'Design with me'},
#     {'id':3 , 'name':'Backend developers'},
# ]



def home(request):
    roomlist = Room.objects.all
    context = {'roomm':roomlist}
    return render(request, 'base/home.html',context)


def room(request , pk ):
    var = Room.objects.get(id=pk)
    context = {'var': var}
    return render(request, 'base/room.html',context)
   
def createRoom(request):                                  #CURD operation(Create)
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)


def updateRoom(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST , instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form' : form}
    return render (request , 'base/room_form.html', context)