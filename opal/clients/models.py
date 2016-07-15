from django.db import models
from events.models import Event

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    # class Meta:
        # ordering = ['last_name']

class Email(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email

class Phone(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.phone
