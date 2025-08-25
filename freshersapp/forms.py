# freshersapp/forms.py
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # NEW
import re

phone_validator = RegexValidator(  # NEW
    regex=r'^\+?\d{10,15}$',
    message="Enter a valid phone number (10–15 digits, optional +)."
)

class CustomUserCreationForm(UserCreationForm):  # CHANGED
    roll_no = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Roll No.', 'class': 'form-group'}),
        label="Roll No."
    )
    name = forms.CharField(  # NEW
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-group'}),
        label="Name"
    )
    email = forms.EmailField(  # CHANGED
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-group'}),
        label="Email"
    )
    year = forms.ChoiceField(  # NEW
        choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')],
        widget=forms.Select(attrs={'class': 'form-group'}),
        label="Year",
    )
    phone_number = forms.CharField(  # NEW
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-group'}),
        label="Phone Number"
    )
    department = forms.ChoiceField(  # CHANGED
        choices=[
            ('', 'Select a department'),
            ('CSE', 'Computer Science Engineering'),
            ('ECE', 'Electronics and Communication Engineering'),
            ('EEE', 'Electrical and Electronics Engineering'),
            ('MECH', 'Mechanical Engineering'),
            ('CIVIL', 'Civil Engineering'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-group'}),
        label="Department",
    )

    password1 = forms.CharField(  # keep same theme
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-group'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-group'}),
    )

    class Meta:  # CHANGED
        model = CustomUser
        fields = ('roll_no', 'name', 'email', 'year', 'phone_number', 'department', 'password1', 'password2')

    def clean_phone_number(self):                            # CHANGED
        phone = self.cleaned_data.get('phone_number', '')
        if not re.fullmatch(r'^\d{10}$', phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone

    def clean_email(self):  # NEW
        email = self.cleaned_data['email'].lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_roll_no(self):  # NEW
        roll_no = self.cleaned_data['roll_no'].strip()
        if CustomUser.objects.filter(roll_no=roll_no).exists():
            raise forms.ValidationError("This roll number is already registered.")
        return roll_no
