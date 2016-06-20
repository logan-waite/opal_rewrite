from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page
            return HttpResponse("Hello, World")
        else:
            # Return a 'disabled account' error messages
            return HttpResponse("User is not active")

    else:
        # Return an 'invalid login' error message
        return HttpResponse("Not a valid login")

def new_user(request):
    return render(request, 'login/new_user.html')

def create_user(request):
    first_name = request.POST['f_name']
    last_name = request.POST['l_name']
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    new_user = User.objects.create_user(username, email, password)
    new_user.first_name = first_name
    new_user.last_name = last_name

    new_user.save()

    return HttpResponse("User created!")
