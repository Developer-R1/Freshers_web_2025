from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-group'}),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-group'}),
    )
    first_name = forms.CharField( 
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-group'}),
    )
    last_name = forms.CharField(  
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-group'}),
    )   
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-group'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-group'}),
    )
    department = forms.ChoiceField(
        choices=[
            ('', 'Select a department'),
            ('CSE', 'Computer Science Engineering'),
            ('ECE', 'Electronics and Communication Engineering'),
            ('EEE', 'Electrical and Electronics Engineering'),
            ('MECH', 'Mechanical Engineering'),
            ('CIVIL', 'Civil Engineering'),
        ],
        required=True, widget=forms.Select(attrs={'class': 'form-group'}),
        label="Department",
        
    )

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')