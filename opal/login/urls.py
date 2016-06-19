from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    # ex: /login/
    url(r'^$', views.index, name='index'),
]
