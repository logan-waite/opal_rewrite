from django.conf.urls import url

from . import views

app_name = 'events'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'new_event_form/$', views.new_event_form, name='new_event_form'),
]
