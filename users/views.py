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
