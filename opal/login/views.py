import os
import logging
import httplib2

from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_orm import Storage
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
# All this stuff happens when a user clicks the "Sign in with Google" button
def google_sign_in(request):
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
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
    # activities = service.activities()
    # activitylist = activities.list(collection='public', userId='me').execute()
    # logging.info(activitylist)

    return redirect('tasks:index')
@python_2_unicode_compatible
def auth_return(request):
  if not xsrfutil.validate_token(settings.SECRET_KEY, bytes(request.GET['state'], 'utf-8'),
                                 request.user):
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.GET)
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
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
    first_name = User.objects.get(username=username).first_name
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page
            messages.success(request, "Welcome back, %s!" % first_name)
            return redirect('tasks:index')
        else:
            # Return a 'disabled account' error messages
            messages.add_message(request, messages.ERROR, 'Your account has been disabled and we are unable to log you in.')
            return redirect('login:index')

    else:
        # Return an 'invalid login' error message
        messages.add_message(request, messages.ERROR, 'Invalid Login Information')
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

    new_user = User.objects.create_user(username, email, password)
    new_user.first_name = first_name
    new_user.last_name = last_name

    new_user.save()

    messages.success(request, "Welcome, %s!" % first_name)

    return redirect("tasks:index")
