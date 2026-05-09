from  django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from .models import User

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        
        user = User.objects.create_user(username=username, email=email, password=password, phone=phone, address=address)
        user.save()
        
        return redirect('home')
    
    return render(request, 'signup.html')

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')