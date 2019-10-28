from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import *


app_name = "capstone"
urlpatterns = [
    url(r'^$', Home, name='home'),

    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^register/$', register_user, name='register'),

]