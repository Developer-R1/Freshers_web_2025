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
from .utils import send_otp


def home(request):
    return render(request, 'home_page.html')


def events(request):
    events = Event.objects.all() 
    return render(request,'events.html',{'events': events})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Temporarily store form data in session
            request.session['signup_data'] = form.cleaned_data  

            # Send OTP
            email = form.cleaned_data.get('email')
            otp = send_otp(email)
            request.session['signup_otp'] = otp  # store OTP in session

            return redirect('verify_otp')  # go to OTP verification page
    else:
        form = CustomUserCreationForm()

    return render(request, 'sign_up.html', {'form': form})


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("signup_otp")
        data = request.session.get("signup_data")

        if entered_otp == session_otp:
            # ✅ OTP matched → create user
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password1'],
            )
            UserProfile.objects.create(user=user, department=data['department'])
            
            # clear session data
            del request.session['signup_data']
            del request.session['signup_otp']

            login(request, user)
            messages.success(request, "Account created successfully 🎉")
            return redirect('events')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')

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
    event.participants = profile.joined_events.count()
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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Send OTP
            otp = send_otp(user.email)
            request.session["login_user_id"] = user.id
            request.session["login_otp"] = otp
            messages.info(request, "OTP sent to your email. Enter it below.")

            return redirect("login_verify_otp")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def login_verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("login_otp")
        user_id = request.session.get("login_user_id")

        if entered_otp == session_otp and user_id:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)

            login(request, user)

            # Clear session
            request.session.pop("login_user_id", None)
            request.session.pop("login_otp", None)

            messages.success(request, "Login successful 🎉")
            return redirect("events")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "login_verify_otp.html")

    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def teams_view(request):
    teams = Team.objects.all()
    teams_by_category = {}
    

    for member in teams:
        category = member.event.title
      
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

