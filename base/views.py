from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .models import Room , Topic
from .forms import RoomForm

    


    