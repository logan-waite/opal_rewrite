from django.db import models


# Create your models here.
# Table for individual checklist items
class Checklist_Item(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

# Table for individual events
class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    checklist_items = models.ManyToManyField(Checklist_Item)

    def __str__(self):
        return self.name

# Places events could be held
class Place(models.Model):
    name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=5, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Events that have been scheduled
class Scheduled_Event(models.Model):
    event = models.ForeignKey(Event)
    place = models.ForeignKey(Place)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.event.name

# The checklist for each scheduled event that can be checked off.
class Scheduled_Event_Checklist(models.Model):
    checklist_item = models.ForeignKey(Checklist_Item)
    scheduled_event = models.ForeignKey(Scheduled_Event)
    completed = models.BooleanField()

    def __str__(self):
        return str(self.checklist_item)

# The checklists for each individual event.
class Event_Checklist(models.Model):
    checklist_item = models.ForeignKey(Checklist_Item)
    event = models.ForeignKey(Event)

    def __str__(self):
        return self.event.name
