from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Event, UserProfile,Team,Web_team
from .forms import CustomUserCreationForm
import json
from django.contrib.auth import logout


def home(request):
    return render(request, 'home_page.html')


def events(request):
    events = Event.objects.all() 
    return render(request,'events.html',{'events': events})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            department = form.cleaned_data.get('department')
            UserProfile.objects.create(user=user, department=department)

            login(request, user) 
            return redirect('events') 
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'sign_up.html', {'form': form})

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)   
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('events')


    if event in profile.joined_events.all():
        messages.info(request, "You've already joined this event.")
        return redirect('events')

    if event.participants >= event.capacity:
        messages.warning(request, "This event is already full.")
        return redirect('events')

    profile.joined_events.add(event)
    event.participants += 1
    event.save()
    profile.save()
    messages.success(request, "Successfully joined the event!")

    # if event.participants_list.filter(id=profile.id).exists():
    #     messages.info(request, "You have already joined this event.")
    
    
    # elif event.participants_list.count() < event.capacity:
    #     event.participants_list.add(profile) 
    #     event.participants = event.participants_list.count() 
    #     messages.success(request, "Successfully joined the event!")
    
    # else:
    #     messages.warning(request, "This event is already full.")

    return redirect('events')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('events')  
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def teams_view(request):
    teams = Team.objects.all()
    teams_by_category = {}

    for member in teams:
        category = member.category.lower()
        if category not in teams_by_category:
            teams_by_category[category] = []
        teams_by_category[category].append(member)

    context = {
        'teams_by_category': teams_by_category,
        'total_members': teams.count(),
        'total_departments': len(teams_by_category),
    }
    return render(request, 'teams.html', context)

def schedule(request):
    return render(request, 'schedule.html')

