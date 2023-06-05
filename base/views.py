from django.shortcuts import render ,redirect
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Q

# roomlist = [
#     {'id':1 , 'name':'Lets Learn Python'},
#     {'id':2 , 'name':'Design with me'},
#     {'id':3 , 'name':'Backend developers'},
# ]



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    roomlist = Room.objects.filter(
    Q(topic__namee__icontains=q) |
    Q(name__icontains=q) |
    Q(description__icontains=q)
    )

    topics = Topic.objects.all()

    room_count = roomlist.count()
    
    context = {'roomm':roomlist , 'topicc':topics ,"room_count":room_count }
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


def updateRoom(request , pk):                              # update
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = RoomForm(request.POST , instance = room )
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form' : form}
    return render (request , 'base/room_form.html', context)



def deleteRoom(request , pk):
    room = Room.objects.get(id = pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render (request , 'base/delete.html',{'obj' : room})