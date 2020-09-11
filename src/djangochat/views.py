from django.shortcuts import render
from django.contrib.auth.models import User 

def home(request):
    count = User.objects.count()  
    return render(request , 'home.html' ,{'count':count})