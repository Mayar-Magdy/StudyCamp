from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room , Topic
from .forms import RoomForm

 

def loginpage(request):
        page = 'login'
        
        if request.user.is_authenticated :
            return redirect('home')
        
        if request.method == 'POST':
            username = request.POST.get('username').lower()
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
        context={'page': page}
        return render(request, 'base/login.html',context)

def logoutpage (request):
            logout(request) 
            return redirect('home')

def registerpage(request): 
    # to be displayed to the user.
    form = UserCreationForm()
    if request.method == 'POST' :
       form = UserCreationForm(request.POST)
       if form.is_valid():
           """This saves the form data to a User object but doesn't commit it to the database yet.
            This allows you to make additional modifications before saving."""
           user = form.save(commit=False)
           user.username =  user.username.lower()
           user.save()
           login(request,user)
           return redirect('home')
       else :
           messages.error(request, 'An error occurred')
    return render(request, 'base/login.html', {'form' : form})


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

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host :
        return HttpResponse('You are not allowed ❌')
    if request.method =='POST':
      form = RoomForm(request.POST, instance=room)
      if form.is_valid():
            form.save()
            return redirect ('home')    
    context = {'form' : form}
    return render(request, 'base/room_form.html',context)

  
@login_required(login_url='login')
def deleteRoom(request , pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse('You are not allowed ❌')
    if request.method == 'POST':
        room.delete()
        return redirect ('home')
    return render(request, 'base/delete.html',{'obj' : room})

    


     