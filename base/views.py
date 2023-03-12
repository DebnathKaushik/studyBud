from django.shortcuts import render



roomlist = [
    {'id':1 , 'name':'Lets Learn Python'},
    {'id':2 , 'name':'Design with me'},
    {'id':3 , 'name':'Backend developers'},
]



def home(request):
    context = {'key_room':roomlist}                       # "room" is context name
    return render(request, 'base/home.html',context)


def room(request , pk ):
    variable_room = None
    for i in roomlist:
        if i['id'] == int(pk):
            variable_room = i
    context = {'key_room': variable_room}
    return render(request, 'base/room.html',context)
   
