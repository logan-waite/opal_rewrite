from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    # ex: /login/
    url(r'^$', views.index, name='index'),
    url(r'^sign_in/$', views.sign_in, name="sign_in"),
    url(r'^new_user/$', views.new_user, name="new_user"),
    url(r'^create_user/$', views.create_user, name="create_user"),
]
