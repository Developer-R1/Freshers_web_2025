# from django.contrib.auth.models import User,AbstractUser
# from django.db import models
# from django.utils import timezone

# class Event(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     date = models.DateField()
#     time = models.TimeField()
#     venue = models.CharField(max_length=255)
#     prize = models.IntegerField()
#     participants = models.IntegerField(default=0)
#     capacity = models.IntegerField()
#     status = models.CharField(choices=[('LIVE','Live'),('UPCOMING','Upcoming')])
#     event_type = models.CharField(choices=[('individual','Individual'),('team','Team')])
#     participants = models.PositiveIntegerField(default=0)  
#     participants_list = models.ManyToManyField('UserProfile', blank=True, related_name='joined_events')



#     def __str__(self):
#         return self.title

# class CustomUser(AbstractUser):
#     username = None   # ❌ remove username
#     last_name = None  # ❌ remove last_name

#     roll_no = models.CharField(max_length=20, unique=True)
#     year = models.IntegerField(choices=[
#         (1, "1st Year"), (2, "2nd Year"),
#         (3, "3rd Year"), (4, "4th Year")
#     ])
#     phone_number = models.CharField(max_length=15, unique=True)
#     department = models.CharField(
#         max_length=50,
#         choices=[
#             ('CSE', 'Computer Science Engineering'),
#             ('ECE', 'Electronics and Communication Engineering'),
#             ('EEE', 'Electrical and Electronics Engineering'),
#             ('MECH', 'Mechanical Engineering'),
#             ('CIVIL', 'Civil Engineering'),
#         ]
#     )

#     # Use roll_no instead of username for login
#     USERNAME_FIELD = 'roll_no'
#     REQUIRED_FIELDS = []   # no required extra fields

#     def __str__(self):
#         return f"{self.roll_no} - {self.department}"
    
# class Team(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
#     team_name = models.CharField(max_length=100)

#     head_name = models.CharField(max_length=100)
#     head_photo = models.ImageField(upload_to='team_heads/')
#     head_linkedin = models.URLField(blank=True, null=True)
#     head_designation = models.CharField(max_length=100, blank=True)
#     category = models.CharField(max_length=100, default="general")

#     def __str__(self):
#         return f"{self.team_name} - {self.head_name}"

# class Web_team(models.Model):
#     name = models.CharField(max_length=100)
#     role = models.CharField(max_length=100) 
#     photo = models.ImageField(upload_to='web_team/')
#     linkedin = models.URLField(blank=True, null=True)
#     github = models.URLField(blank=True, null=True)  
#     email = models.EmailField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - {self.role}"

# class EventRegistration(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     registered_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending')])

#     class Meta:
#         unique_together = ('user_profile', 'event')  

#     def __str__(self):
#         return f"{self.user_profile.user.username} - {self.event.name}"


# freshersapp/models.py
from django.conf import settings 
from django.contrib.auth.models import AbstractUser, BaseUserManager  
from django.db import models
from django.db.models.signals import post_save, post_delete  
from django.dispatch import receiver

class Event(models.Model):
    title = models.CharField(max_length=255)
    club = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    prize = models.IntegerField()
    capacity = models.IntegerField()
    status = models.CharField(choices=[('LIVE', 'Live'), ('UPCOMING', 'Upcoming')])
    event_type = models.CharField(choices=[('club', 'Club Event'), ('non_club', 'Non Club Event')])
    participants = models.PositiveIntegerField(default=0)

    coordinator1 = models.CharField(max_length=100, blank=True, null=True)
    coordinator2 = models.CharField(max_length=100, blank=True, null=True)
    coordinator3 = models.CharField(max_length=100, blank=True, null=True)
    coordinator4 = models.CharField(max_length=100, blank=True, null=True)
    coordinator1_phone = models.CharField(max_length=15, blank=True, null=True)
    coordinator2_phone = models.CharField(max_length=15, blank=True, null=True)
    coordinator3_phone = models.CharField(max_length=15, blank=True, null=True)
    coordinator4_phone = models.CharField(max_length=15, blank=True, null=True)


    participants_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='EventRegistration', related_name='events_joined'
    )

    # def is_coordinator(self, user):
    #     return self.eventcoordinator_set.filter(user=user).exists()

    def __str__(self):
        return self.title

    @property 
    def events_joined_list(self):
        return list(self.joined_events.values_list('title', flat=True))
    
class EventCoordinator(models.Model):  
    """Who can download CSV for an event (access per-event)."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='coordinators')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coordinated_events')

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.roll_no} -> {self.event.title}"




class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, roll_no, name, email, year, phone_number, department, password=None, **extra_fields):
        if not roll_no:
            raise ValueError("Roll number is required")
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            roll_no=roll_no,
            name=name,
            email=email,
            year=year,
            phone_number=phone_number,
            department=department,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, roll_no, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault("email", "admin@example.com")
        extra_fields.setdefault("year", 1)
        extra_fields.setdefault("department", "CSE")

        if not extra_fields.get("phone_number"):
            raise ValueError("Superuser must have a phone number")

        return self.create_user(roll_no=roll_no, password=password, **extra_fields)



class CustomUser(AbstractUser):  
    username = None  
    last_name = None  

    roll_no = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=150)  
    email = models.EmailField(unique=True) 
    year = models.IntegerField(choices=[(1,"1st Year"), (2,"2nd Year"), (3,"3rd Year"), (4,"4th Year")])  
    phone_number = models.CharField(max_length=15, unique=True)  
    department = models.CharField(  
        max_length=50,
        choices=[
            ('CSE', 'Computer Science Engineering'),
            ('ECE', 'Electronics and Communication Engineering'),
            ('EEE', 'Electrical and Electronics Engineering'),
            ('MECH', 'Mechanical Engineering'),
            ('CIVIL', 'Civil Engineering'),
            ('BSC/B.ED','Education Department'),

        ],
    )
    # can_download_csv = models.BooleanField(default=False)  

    
    # joined_events = models.ManyToManyField("Event", through="EventRegistration", related_name="participants")  

    USERNAME_FIELD = 'roll_no' 
    REQUIRED_FIELDS = ['name', 'email','phone_number'] 

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
    
    @property 
    def events_joined_list(self):
        return list(self.joined_events.values_list('title', flat=True))


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=100)
    head_name = models.CharField(max_length=100)
    head_photo = models.ImageField(upload_to='team_heads/')
    head_linkedin = models.URLField(blank=True, null=True)
    head_designation = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, default="general")

    def __str__(self):
        return f"{self.team_name} - {self.head_name}"


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
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('pending', 'Pending')])

    class Meta:
        unique_together = ('user', 'event') 

    def __str__(self):
        return f"{self.user.roll_no} - {self.event.title}"  

class CoreCommittee(models.Model):   
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="core_committee/")  
 

    def __str__(self):
        return f"{self.name} - {self.role}"

class WebTeam(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='web_team_images/')
    linkedin_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

@receiver(post_save, sender=EventRegistration) 
def _sync_event_participants_on_save(sender, instance, created, **kwargs): 
    event = instance.event  
    event.participants = event.participants_list.count()  
    event.save(update_fields=['participants'])  

@receiver(post_delete, sender=EventRegistration) 
def _sync_event_participants_on_delete(sender, instance, **kwargs): 
    event = instance.event  
    event.participants = event.participants_list.count()  
    event.save(update_fields=['participants']) 