from django.shortcuts import render ,redirect
from .models import Room,Topic,Meassage
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

# roomlist = [
#     {'id':1 , 'name':'Lets Learn Python'},
#     {'id':2 , 'name':'Design with me'},
#     {'id':3 , 'name':'Backend developers'},
# ]




# This is custom Decorator 
def my_decorator(func):
    def inner(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return func(request,*args,**kwargs)     
    return inner


#This is Loginview/Loginpage
def LoginPage(request):
    page = 'login'
    if request.method == 'POST':
        var_username = request.POST.get('username').lower()   
        var_password = request.POST.get('password')

        try:
            user = User.objects.get(username=var_username) # username is User Model field here 
        except:
            messages.error(request, "User not found")  # if message have then output(main.html)

        user = authenticate(request, username=var_username, password=var_password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "")

    # when user login it doesn't go /login/ url 
    if request.user.is_authenticated:  
        return redirect('home') 
    
    context={'pagee':page}
    return render(request , 'base/login_register.html', context)

    


#This is logoutpage/logoutview
def LogoutPage(request):
    logout(request)
    return redirect('home')


# This is for User registation
def RegisterPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() # this username is usercreatioform model/class field
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error during registration")

    return render(request, 'base/login_register.html',{'form':form})



#Homepage
def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    roomlist = Room.objects.filter(
    Q(topic__namee__icontains=q) |
    Q(name__icontains=q) |         # from this Query for search room box (GET perameter/q)
    Q(description__icontains=q)|
    Q(host__username__icontains=q)
    )

    # For Add Topic
    # if request.method == 'POST': 
    #     new_topic = request.POST.get('topic_name')
    #     if new_topic:
    #         try:
    #             Topic.objects.get(namee=new_topic)
    #         # Topic already exists, handle the case accordingly
    #         # For example, you can display an error message or take a different action
    #             pass
    #         except Topic.DoesNotExist:
    #             Topic.objects.create(namee=new_topic)
    #         # Topic was successfully created
    #         # Handle the case when a new topic is created
            
           
    # # For Delete Topic 
    # if request.method == 'POST':
    #     delete_topic = request.POST.get("delete_topic")
    #     if delete_topic:
    #         try:
    #             topic = Topic.objects.get(namee=delete_topic)
    #             topic.delete()
    #         except Topic.DoesNotExist:
    #             return HttpResponse("Topic not found")
             
    topics = Topic.objects.all()
    room_count = roomlist.count()
    room_messages = Meassage.objects.filter(
         Q(room__topic__namee__icontains=q)
        )
    
    context = {'roomm':roomlist , 'topicc':topics ,"room_count":room_count,'room_messages':room_messages}
    return render(request, 'base/home.html',context)

#Go to Room
def room(request , pk ):
    var_room = Room.objects.get(id=pk)
    room_messages = var_room.meassage_set.all()# This is related manager for foreign key(meassage_set)
    room_participants = var_room.participants.all()

    if request.method == "POST":
        room_messages = Meassage.objects.create(
            user = request.user,
            room = var_room,
            body = request.POST.get('body')
            )
        var_room.participants.add(request.user)#participants it just Room Model attribute(related manager)
        return redirect ('room', pk=var_room.id)
    

    context = {'var_room': var_room, 'room_messages':room_messages,'room_participants':room_participants}
    return render(request, 'base/room.html',context)
   

#This is for User Profile
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    roomlist = user.room_set.all()
    room_messages = user.meassage_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'roomm':roomlist,'room_messages':room_messages,'topicc':topics}
    return render (request,'base/profile.html',context)


#This is for create Room
@my_decorator
def createRoom(request):                 
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        topic_name = request.POST.get('TOPIC')
        TOPIC,created = Topic.objects.get_or_create(namee = topic_name)

        Room.objects.create(
            host = request.user,
            topic = TOPIC,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {'form':form , 'topicc':topics}
    return render(request, 'base/room_form.html',context)


#This is for update Room
@my_decorator
def updateRoom(request , pk):                              
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        topic_name = request.POST.get('TOPIC')
        TOPIC,created = Topic.objects.get_or_create(namee = topic_name)
        room.name = request.POST.get('name')
        room.topic = TOPIC
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form' : form ,'topicc':topics, 'room':room }
    return render (request , 'base/room_form.html', context)


#This is for delete Room
@my_decorator
def deleteRoom(request , pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render (request , 'base/delete.html',{'obj' : room})


#This is delete for Room_Message 
@my_decorator
def deleteMessage(request , pk):
    message = Meassage.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render (request , 'base/delete.html',{'obj' : message})


# this is for when message delete in room and back to same room/And (after complete next task -> recent activity message delete will be upper one.)
# change will be (url,home templte{delete link},viwes name)
# @my_decorator
# def deleteMessage(request , pk):
#     message = Meassage.objects.get(id = pk)

#     if request.user != message.user:
#         return HttpResponse("You are not allowed here")

#     if request.method == 'POST':
#         room_id = message.room.id
#         message.delete()
#         return redirect('room',pk=room_id)
    
#     return render (request , 'base/delete.html',{'obj' : message})

