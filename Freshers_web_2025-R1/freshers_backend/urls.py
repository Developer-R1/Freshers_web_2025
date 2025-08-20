from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from freshersapp.views import events,join_event,signup,home,login_view,teams_view,schedule,logout_view,about
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('signup/',signup,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/', logout_view, name='logout'),
    path('schedule/',schedule,name='schedule'),
    path('events/',events,name='events'),
    path('teams/',teams_view,name='teams'),
    path('join-event/<int:event_id>/',join_event, name='join_event'),
    path('about/',about,name='about'),

]
