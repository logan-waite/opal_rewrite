from django.db import models
from events.models import Event

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email1 = models.CharField(max_length=50)
    email2 = models.CharField(max_length=50)
    phone1 = models.CharField(max_length=10)
    phone2 = models.CharField(max_length=10)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    events = models.ManyToManyField(Event)
