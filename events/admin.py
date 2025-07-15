from django.contrib import admin
from .models import Event

@admin.register(Event)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','date', 'time', 'venue','prize','participants','capacity','status','event_type')
    search_fields = ('title',)