from django.contrib import admin
from .models import Event,Team,Web_team,UserProfile

@admin.register(Event)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','date', 'time', 'venue','prize','participants','capacity','status','event_type')
    search_fields = ('title',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'head_designation', 'head_linkedin')
    search_fields = ('team_name', 'head_designation')

# @admin.register(Web_team)
# class WebTeamAdmin(admin.ModelAdmin):
#     list_display = ('name','role','image','linkedin')
#     search_fields = ('name', 'role')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')
    search_fields = ('user__username', 'department')