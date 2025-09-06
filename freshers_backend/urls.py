from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from freshersapp.views import events,join_event,signup,home,login_view,teams_view,schedule,logout_view,verify_otp,login_verify_otp,download_event_csv, profile,corecom, webteam,forgot_password ,forgot_password_verify,reset_password
from django.contrib.auth import views as auth_views
from django.shortcuts import render

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
    path("core-committee/", corecom, name="core_committee"),
    path("webteam/", webteam, name="webteam"),
    path('contacts/', lambda request: render(request, 'contact_us.html'), name='contacts'),
    path("forgot-password/", forgot_password, name="forgot_password"), 
    path("forgot-password-verify/", forgot_password_verify, name="forgot_password_verify"),
    path("reset-password/", reset_password, name="reset_password"),  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
