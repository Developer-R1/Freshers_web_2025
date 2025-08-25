from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from freshersapp.views import events,join_event,signup,home,login_view,teams_view,schedule,logout_view,verify_otp,login_verify_otp,download_event_csv, profile 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('signup/',signup,name='signup'),
    path('login/',login_view,name='login'),
    path("login/verify-otp/",login_verify_otp, name="login_verify_otp"),
    path('logout/', logout_view, name='logout'),
    path('schedule/',schedule,name='schedule'),
    path('events/',events,name='events'),
    path('teams/',teams_view,name='teams'),
    path('events/<int:event_id>/join', join_event, name='join_event'),
    # path('join-event/<int:event_id>/',join_event, name='join_event'),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path('events/<int:event_id>/download_csv', download_event_csv, name='download_event_csv'),
    path('profile/', profile, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
