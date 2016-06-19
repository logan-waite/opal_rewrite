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
            pass

    else:
        # Return an 'invalid login' error message
        return HttpResponse("Not a valid login")
