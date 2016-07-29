from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    checklist_items = models.ManyToManyField(Checklist_Item);

class Place(models.Model):
    name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=5, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=50)

class Checklist_Item(models.Model):
    name = models.CharField(max_length=50)

class Scheduled_Event:
    event = models.ForeignKey(Event)
    place = models.ForeignKey(Place)
    start = models.DateTimeField()
    end = models.DateTimeField()

class Scheduled_Event_Checklist:
    checklist_item = models.ForeignKey(Checklist_Item)
    scheduled_event = models.ForeignKey(Scheduled_Event)
    completed = models.BooleanField()
