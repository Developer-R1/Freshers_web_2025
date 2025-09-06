# from django.contrib import admin
# from .models import Event,Team,CustomUser

# @admin.register(Event)
# class ClassAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description','date', 'time', 'venue','prize','participants','capacity','status','event_type')
#     search_fields = ('title',)

# @admin.register(Team)
# class TeamAdmin(admin.ModelAdmin):
#     list_display = ('team_name', 'head_designation', 'head_linkedin')
#     search_fields = ('team_name', 'head_designation')

# # @admin.register(Web_team)
# # class WebTeamAdmin(admin.ModelAdmin):
# #     list_display = ('name','role','image','linkedin')
# #     search_fields = ('name', 'role')


# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ("roll_no", "name", "year", "email", "phone_no", "department")
#     search_fields = ("roll_no", "name", "email", "phone_no", "department")


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Event, Team, Web_team, CustomUser,EventCoordinator,CoreCommittee,WebTeam,EventRegistration   

class EventRegistrationInlineForEvent(admin.TabularInline): 
    model = EventRegistration
    fk_name = "event" 
    extra = 0
    autocomplete_fields = ["user"] 
    verbose_name = "Participant" 
    verbose_name_plural = "Participants" 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):  
    list_display = ('title', 'description', 'date', 'time', 'venue', 'prize', 'participants', 'capacity', 'status', 'event_type')
    search_fields = ('title',)

    inlines = [EventRegistrationInlineForEvent]

class EventRegistrationInlineForUser(admin.TabularInline): 
    model = EventRegistration
    fk_name = "user"  
    extra = 0
    autocomplete_fields = ["event"]  
    verbose_name = "Joined Event"  
    verbose_name_plural = "Joined Events"  

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'head_designation', 'head_linkedin')
    search_fields = ('team_name', 'head_designation')

@admin.register(Web_team)
class WebTeamAdmin(admin.ModelAdmin):  
    list_display = ('name','role','email')
    search_fields = ('name', 'role')

@admin.register(CustomUser)  
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('roll_no', 'name', 'email', 'year', 'phone_number', 'department', 'is_staff', 'is_active')
    search_fields = ('roll_no', 'name', 'email', 'phone_number')
    ordering = ('roll_no',)

    fieldsets = (  
        (None, {'fields': ('roll_no', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'year', 'phone_number', 'department')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = ( 
        (None, {
            'classes': ('wide',),
            'fields': ('roll_no', 'name', 'email', 'year', 'phone_number', 'department', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    inlines = [EventRegistrationInlineForUser]


@admin.register(EventCoordinator) 
class EventCoordinatorAdmin(admin.ModelAdmin):
    list_display = ('event', 'user')
    search_fields = ('event__title', 'user__roll_no')



@admin.register(CoreCommittee)     
class CoreCommitteeAdmin(admin.ModelAdmin):
    list_display = ("name", "role")   
    search_fields = ("name", "role")  


@admin.register(WebTeam)
class WebTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'linkedin_link')