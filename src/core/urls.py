from django.urls import path 
from . import views 

app_name = 'core'
urlpatterns  = [
    path('' , views.register , name ='register'),
    path('profile/' , views.profile, name='profile') 
]