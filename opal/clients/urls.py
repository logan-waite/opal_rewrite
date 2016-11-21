from django.conf.urls import url

from . import views

app_name = 'clients'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'add_client/$', views.add_client, name='add_client'),
    url(r'add_client_submit/$', views.add_client_submit, name='add_client_submit'),
    url(r'get_clients/$', views.get_clients, name='get_clients'),
    url(r'client_info/$', views.client_info, name='client_info'),
    url(r'edit_client/$', views.edit_client, name='edit_client'),
    url(r'edit_client_submit/$', views.edit_client_submit, name='edit_client_submit'),
    url(r'add_product/$', views.add_product, name='add_product'),
    url(r'add_product_submit/$', views.add_product_submit, name='add_product_submit')
]
