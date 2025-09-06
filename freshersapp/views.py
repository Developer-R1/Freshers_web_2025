# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render,redirect,get_object_or_404
# from django.contrib.auth import authenticate, login
# from django.http import HttpResponse,HttpResponseForbidden
# from django.contrib import messages
# from django.views.decorators.http import require_POST
# from .models import Event, CustomUser,Team
# from .forms import CustomUserCreationForm
# import json
# from django.contrib.auth import logout
# from .utils import send_otp


# def home(request):
#     return render(request, 'home_page.html')


# def events(request):
#     events = Event.objects.all() 
#     return render(request,'events.html',{'events': events})

# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Temporarily store form data in session
#             request.session['signup_data'] = form.cleaned_data  

#             # Send OTP
#             email = form.cleaned_data.get('email')
#             otp = send_otp(email)
#             request.session['signup_otp'] = otp  # store OTP in session

#             return redirect('verify_otp')  # go to OTP verification page
#     else:
#         form = CustomUserCreationForm()

#     return render(request, 'sign_up.html', {'form': form})


# def verify_otp(request):
#     if request.method == "POST":
#         entered_otp = request.POST.get("otp")
#         session_otp = request.session.get("signup_otp")
#         data = request.session.get("signup_data")
#         if entered_otp == session_otp:
#             user = CustomUser.objects.create_user(
#                 roll_no=data['roll_no'],
#                 name=data['name'],
#                 year=data['year'],
#                 email=data['email'],
#                 phone_no=data['phone_no'],
#                 department=data['department'],
#                 password=data['password1'],
#             )
#             del request.session['signup_data']
#             del request.session['signup_otp']
#             login(request, user)
#             return redirect('events')
#         else:
#             messages.error(request, "Invalid OTP. Please try again.")
#     return render(request, 'verify_otp.html')

# @login_required
# # def join_event(request, event_id):
# #     event = get_object_or_404(Event, id=event_id)   
# #     try:
# #         profile = UserProfile.objects.get(user=request.user)
# #     except UserProfile.DoesNotExist:
# #         messages.error(request, "User profile not found.")
# #         return redirect('events')


# #     if event in profile.joined_events.all():
# #         messages.info(request, "You've already joined this event.")
# #         return redirect('events')

# #     if event.participants >= event.capacity:
# #         messages.warning(request, "This event is already full.")
# #         return redirect('events')

# #     profile.joined_events.add(event)
# #     event.participants = profile.joined_events.count()
# #     event.save()
# #     profile.save()
# #     messages.success(request, "Successfully joined the event!")

# #     # if event.participants_list.filter(id=profile.id).exists():
# #     #     messages.info(request, "You have already joined this event.")
    
    
# #     # elif event.participants_list.count() < event.capacity:
# #     #     event.participants_list.add(profile) 
# #     #     event.participants = event.participants_list.count() 
# #     #     messages.success(request, "Successfully joined the event!")
    
# #     # else:
# #     #     messages.warning(request, "This event is already full.")

# #     return redirect('events')

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Send OTP
#             otp = send_otp(user.email)
#             request.session["login_user_id"] = user.id
#             request.session["login_otp"] = otp
#             messages.info(request, "OTP sent to your email. Enter it below.")

#             return redirect("login_verify_otp")
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, "login.html")


# def login_verify_otp(request):
#     if request.method == "POST":
#         entered_otp = request.POST.get("otp")
#         session_otp = request.session.get("login_otp")
#         user_id = request.session.get("login_user_id")

#         if entered_otp == session_otp and user_id:
#             from django.contrib.auth.models import User
#             user = User.objects.get(id=user_id)

#             login(request, user)

#             # Clear session
#             request.session.pop("login_user_id", None)
#             request.session.pop("login_otp", None)

#             messages.success(request, "Login successful 🎉")
#             return redirect("events")
#         else:
#             messages.error(request, "Invalid OTP. Please try again.")

#     return render(request, "login_verify_otp.html")

    
# def logout_view(request):
#     if request.user.is_authenticated:
#         logout(request)
#     return redirect('home')

# def teams_view(request):
#     teams = Team.objects.all()
#     teams_by_category = {}
    

#     for member in teams:
#         category = member.event.title
      
#         if category not in teams_by_category:
#             teams_by_category[category] = []
#         teams_by_category[category].append(member)

#     context = {
#         'teams_by_category': teams_by_category,
#         'total_members': teams.count(),
#         'total_departments': len(teams_by_category),
#     }
#     return render(request, 'teams.html', context)

# def schedule(request):
#     return render(request, 'schedule.html')







# freshersapp/views.py
import csv
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,HttpResponseForbidden
from django.contrib import messages
from .models import Event, Team, Web_team, CustomUser,EventRegistration,EventCoordinator,CoreCommittee,WebTeam 
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from .utils import send_otp
from django.db.models import F 
from django.utils.encoding import smart_str 
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'home_page.html')
def events(request):
    user = request.user
    events = Event.objects.all()

    for event in events:
        if user.is_authenticated:  
            event.is_user_coordinator = EventCoordinator.objects.filter(
                event=event, user=user
            ).exists()
        else:
            event.is_user_coordinator = False

    alert = request.GET.get('alert')
    return render(request, 'events.html', {'events': events, 'alert': alert})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data  
            request.session['signup_data'] = {  
                'roll_no': data['roll_no'],
                'name': data['name'],
                'email': data['email'],
                'year': int(data['year']),
                'phone_number': data['phone_number'],
                'department': data['department'],
                'password1': data['password1'],
            }
            otp = send_otp(data['email'])  
            request.session['signup_otp'] = otp
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("signup_otp")
        data = request.session.get("signup_data")
        if entered_otp == session_otp and data:
           
            user = CustomUser.objects.create_user(  
                roll_no=data['roll_no'],
                name=data['name'],
                email=data['email'],
                year=int(data['year']),
                phone_number=data['phone_number'],
                department=data['department'],
                password=data['password1'],
            )
           
            request.session.pop('signup_data', None)
            request.session.pop('signup_otp', None)
            login(request, user)
            messages.success(request, "Account created successfully 🎉")
            return redirect('events')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'verify_otp.html')

@login_required
def join_event(request, event_id):
   
    with transaction.atomic():                                         
        event = Event.objects.select_for_update().get(id=event_id)      
        user = request.user

        if event.participants_list.filter(id=user.id).exists():
            return redirect('/events?alert=' + 'You have already joined this event.')  

        if event.participants >= event.capacity:
            return redirect('/events?alert=' + 'This event is already full.')          

        event.participants_list.add(user)
        event.participants = event.participants_list.count()
        event.save()

        EventRegistration.objects.get_or_create(                        
            user=user, event=event, defaults={'status': 'confirmed'}
        )

    return redirect('/events?alert=' + 'Successfully joined the event!')


@login_required
def download_event_csv(request, event_id):                               
    """Only users added as coordinators for the event can download CSV."""
    event = get_object_or_404(Event, id=event_id)
    allowed = EventCoordinator.objects.filter(event=event, user=request.user).exists()
    if not allowed:
        return HttpResponseForbidden("You do not have access to download this event's CSV.")

   
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{smart_str(event.title)}_registrations.csv"'
    writer = csv.writer(response)
    writer.writerow(['Roll No', 'Name', 'Email', 'Phone', 'Year', 'Department', 'Registered At', 'Status'])

    regs = EventRegistration.objects.filter(event=event).select_related('user')
    for r in regs:
        writer.writerow([
            r.user.roll_no,
            r.user.name,
            r.user.email,
            r.user.phone_number,
            r.user.year,
            r.user.department,
            r.registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            r.status,
        ])
    return response

@login_required
def profile(request):
   
    user = request.user
    events = EventRegistration.objects.filter(user=user)
    
    return render(request, 'profile.html', {
        'user': user,
        'events': events
    })

def login_view(request):
    if request.method == "POST":
        
        roll_no = request.POST.get("roll_no")  
        password = request.POST.get("password")
      
        user = authenticate(request, username=roll_no, password=password)  

        if user is not None:
            otp = send_otp(user.email)
            request.session["login_user_id"] = user.id
            request.session["login_otp"] = otp
            messages.info(request, "OTP sent to your email. Enter it below.")
            return redirect("login_verify_otp")
        else:
            messages.error(request, "Invalid roll number or password.")
            return redirect("login")
    return render(request, "login.html")

def login_verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("login_otp")
        user_id = request.session.get("login_user_id")
        if entered_otp == session_otp and user_id:
            user = CustomUser.objects.get(id=user_id)
            login(request, user)
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
        teams_by_category.setdefault(category, []).append(member)

    core_committee = CoreCommittee.objects.all().order_by("id")
    web_team = WebTeam.objects.all().order_by("id")

    context = {
        'teams_by_category': teams_by_category,
        'core_committee': core_committee,  
        'web_team': web_team,               
    }
    return render(request, 'teams.html', context)

def schedule(request):
    return render(request, 'schedule.html')


def corecom(request):
    members = CoreCommittee.objects.all().order_by("id") 
    return render(request, 'corecompage.html', {"core_committee": members}) 

def webteam(request):  
    members = Web_team.objects.all().order_by("id")   
    return render(request, 'webteam.html', {"web_team": members})


def forgot_password(request):
    if request.method == "POST":
        roll_no = request.POST.get("roll_no")
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(roll_no=roll_no, email=email)
            otp = send_otp(email)
            request.session["forgot_user_id"] = user.id
            request.session["forgot_otp"] = otp
            messages.info(request, "OTP sent to your email.")
            return redirect("forgot_password_verify")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found. Check roll no and email.")
    return render(request, "forgot_password.html") 


def forgot_password_verify(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("forgot_otp")
        if entered_otp == session_otp:
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP. Try again.")
    return render(request, "forgot_password_verify.html")


def reset_password(request):
    if request.method == "POST":
        new_pass = request.POST.get("password1")
        confirm_pass = request.POST.get("password2")
        if new_pass == confirm_pass:
            user_id = request.session.get("forgot_user_id")
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                user.password = make_password(new_pass)
                user.save()
               
                request.session.pop("forgot_user_id", None)
                request.session.pop("forgot_otp", None)
                messages.success(request, "Password reset successful. Login again.")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "reset_password.html")


