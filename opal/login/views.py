import os
import logging
import httplib2

from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets

from oauth2client.contrib.django_util.storage import DjangoORMStorage

from opal import settings

from .models import User, CredentialsModel

# Google API stuff
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calendar https://mail.google.com',
    redirect_uri='http://127.0.0.1:8080/login/oauth2callback'
    )

# ----------------------------------------------------------------------------
# If a user changes their mind, but is already logged in.
@python_2_unicode_compatible
def google_sign_in(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("calendar", "v3", http=http)
        return redirect("tasks:index")

# When the user comes back from allowing or denying permissions.
@python_2_unicode_compatible
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, bytes(request.GET['state'], 'utf-8'),
                                request.user):
        return  HttpResponseBadRequest()
    try:
        credential = FLOW.step2_exchange(request.GET)
    except:
        return render(request, 'login/denied_access.html')
    else:
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        storage.put(credential)
        return redirect("tasks:index")
# ----------------------------------------------------------------------------


# Main Login page
def index(request):
    return render(request, 'login/index.html')

# Script to check if user is able to sign in.
def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            first_name = User.objects.get(username=username).first_name

            # Google sign_in code
            storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
            credential = storage.get()
            if credential is None or credential.invalid == True:
                FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                           request.user)
                authorize_url = FLOW.step1_get_authorize_url()
                return HttpResponseRedirect(authorize_url)
            else:
                http = httplib2.Http()
                http = credential.authorize(http)
                service = build("calendar", "v3", http=http)
            # Redirect to a success page
                messages.info(request, "Welcome back, %s!" % first_name)
            return redirect('tasks:index')
        else:
            # Return a 'disabled account' error messages
            messages.add_message(request, messages.ERROR, 'Your account has been disabled and we are unable to log you in.')
            return redirect('login:index')

    else:
        # Return an 'invalid login' error message
        messages.add_message(request, messages.ERROR, 'Invalid Login Information, please try again')
        return redirect('login:index')

# Load the new user page
def new_user(request):
    return render(request, 'login/new_user.html')

# Creates a user and logs them in.
def create_user(request):
    first_name = request.POST['f_name']
    last_name = request.POST['l_name']
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    try:
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
    except Exception as e:
        print(e)
        if str(e).find('username'):
            messages.error(request, "That username is already in use")
        return redirect('login:new_user')

    # Log the new user in so the system doesn't freak out
    user = authenticate(username=username, password=password)
    login(request, user)

    # Google sign-in code
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("calendar", "v3", http=http)

    messages.info(request, "Welcome, %s!" % first_name)

    return redirect("tasks:index")

def google_deny(request):
    curr_user = request.user
    user = User.objects.get(username=curr_user)
    logout(request)
    user.delete()
    return redirect("login:index")

def user_logout(request):
    logout(request)
    return redirect('login:index')
