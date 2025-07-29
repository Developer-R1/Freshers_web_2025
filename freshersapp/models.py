from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    prize = models.IntegerField()
    participants = models.IntegerField(default=0)
    capacity = models.IntegerField()
    status = models.CharField(max_length=255,choices=[('LIVE','Live'),('UPCOMING','Upcoming')])
    event_type = models.CharField(max_length=255,choices=[('individual','Individual'),('team','Team')])
    participants = models.PositiveIntegerField(default=0)  
    participants_list = models.ManyToManyField('UserProfile', blank=True, related_name='joined_events')



    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    booked_events = models.ManyToManyField(Event, blank=True, related_name='booked_users')

    def __str__(self):
        return self.user.username
    
class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=100)

    head_name = models.CharField(max_length=100)
    head_photo = models.ImageField(upload_to='team_heads/')
    head_linkedin = models.URLField(blank=True, null=True)
    head_designation = models.CharField(max_length=100, blank=True)

class Web_team(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100) 
    photo = models.ImageField(upload_to='web_team/')
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)  
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class EventRegistration(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending')])

    class Meta:
        unique_together = ('user_profile', 'event')  

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.event.name}"

