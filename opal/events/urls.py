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
    url(r'edit_events/$', views.edit_events, name='edit_events'),
    url(r'get_event_info/$', views.get_event_info, name='get_event_info'),
    url(r'new_checklist_item/$', views.new_checklist_item, name='new_checklist_item'),
    url(r'edit_event_submit/$', views.edit_event_submit, name='edit_event_submit'),
    url(r'save_item_status/$', views.save_item_status, name='save_item_status'),
    url(r'get_scheduled_events/$', views.get_scheduled_events, name='get_scheduled_events'),
]
