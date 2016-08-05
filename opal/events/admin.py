from django.contrib import admin

from .models import Event, Place, Checklist_Item, Scheduled_Event, Scheduled_Event_Checklist, Event_Checklist
# Register your models here.

admin.site.register(Event)
admin.site.register(Place)
admin.site.register(Checklist_Item)
admin.site.register(Scheduled_Event)
admin.site.register(Scheduled_Event_Checklist)
admin.site.register(Event_Checklist)
