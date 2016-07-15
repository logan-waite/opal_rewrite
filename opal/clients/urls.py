from django.conf.urls import url

from . import views

app_name = 'clients'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'add_client/$', views.add_client, name='add_client'),
    url(r'add_client_submit/$', views.add_client_submit, name='add_client_submit'),
    url(r'get_clients/$', views.get_clients, name='get_clients'),
    url(r'client_info/$', views.client_info, name='client_info')
]
