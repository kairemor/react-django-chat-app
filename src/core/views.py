from django.shortcuts import render , redirect  
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = UserCreationForm()
    args = {'form': form}
    return render(request , 'register.html', args)    

def profile(request):
    return render(request, 'profile.html')