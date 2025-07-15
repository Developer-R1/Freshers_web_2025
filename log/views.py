from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Home view (optional login required)
def home(request):
    return render(request, "registration/home.html")

#schedule view
def schedule(request):
    return render(request, "registration/schedule.html")

def event(request):
    return render(request, "registration/events.html")

# Login view
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("frontpage")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "registration/login.html")  # Don't redirect — re-render with message
    else:
        return render(request, "registration/login.html")



def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("frontpage")
        
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/demo.html", {
        "form": form,
    })

# Logout view
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("frontpage")
