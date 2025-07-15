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
    status = models.CharField(choices=[('LIVE','Live'),('UPCOMING','Upcoming')])
    event_type = models.CharField(choices=[('individual','Individual'),('team','Team')])


    def __str__(self):
        return self.title