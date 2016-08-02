from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'new_event_form/$', views.new_event_form, name='new_event_form'),
    url(r'new_event_submit/$', views.new_event_submit, name='new_event_submit'),
    url(r'schedule_event_form/$', views.schedule_event_form, name='schedule_event_form'),
    url(r'schedule_event_submit/$', views.schedule_event_submit, name='schedule_event_submit'),
    url(r'add_place/$', views.add_place, name='add_place'),
]
