from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Event

def events(request):
    events = Event.objects.all() 
    return render(request,'events.html',{'events': events})


