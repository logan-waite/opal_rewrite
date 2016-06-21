from django.db import models
from django.contrib.auth.models import User
from oauth2client.contrib.django_orm import CredentialsField, FlowField

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=150)

class CredentialsModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()

class FlowModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    flow = FlowField()
