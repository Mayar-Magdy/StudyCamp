from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .models import Room , Topic
from .forms import RoomForm


# Create your views here.

# rooms = [
#     {'id' : 1 , 'name': 'python' },
#     {'id' : 2 , 'name': 'java' },
#     {'id' : 3 , 'name': 'Ruby' },
# ]

def loginpage(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            isUser = False

            try :
                user = User.objects.get(username=username)
                isUser = True
            except :
                messages.error(request  , "User doesn't exist")
                

            if isUser :
             user = authenticate(request, username=username, password=password)
            
             if user is not None :
                login(request, user)
                return redirect('home')
             else :
                messages.error(request  , "Username or Password doesn't exist ")

        return render(request, 'base/login.html')

def logoutpage (request):
            logout(request) 
            return render(request, 'base/login.html')
def home(request):
    q= request.GET.get('q') if (request.GET.get('q') != None)  else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) )
    Topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms' :rooms ,"Topics":Topics , 'room_count' :room_count }
    return render(request, 'home.html',context)

def room(request ,pk):
   room = Room.objects.get(id=pk)
   context = { 'room' : room }
   return render(request, 'room.html',context)

@login_required(login_url='login')
def createRoom (request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('home')
        
    context = {'form' : form }
    return render(request, 'base/room_form.html',context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method =='POST':
      form = RoomForm(request.POST, instance=room)
      if form.is_valid():
            form.save()
            return redirect ('home')    
    context = {'form' : form}
    return render(request, 'base/room_form.html',context)

def deleteRoom(request , pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect ('home')
    return render(request, 'base/delete.html',{'obj' : room})

    


    