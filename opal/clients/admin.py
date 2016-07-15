from django.contrib import admin

from .models import Client, Email, Phone
# Register your models here.

admin.site.register(Client)
admin.site.register(Email)
admin.site.register(Phone)
