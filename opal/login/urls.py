from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    # ex: /login/
    url(r'^$', views.index, name='index'),
    #ex: /login/sign_in/
    url(r'^sign_in/$', views.sign_in, name="sign_in"),
    #ex: /login/new_user/
    url(r'^new_user/$', views.new_user, name="new_user"),
    #ex: /login/create_user/
    url(r'^create_user/$', views.create_user, name="create_user"),
    # google auth
    url(r'^oauth2callback/$', views.auth_return, name='auth_return'),
    # Allow after denying google
    url(r'^google_allow/$', views.google_sign_in, name='google_sign_in'),
    # Deny's Google completely
    url(r'^google_deny/$', views.google_deny, name='google_deny'),
    # ex: /login/logout
    url(r'^logout/$', views.user_logout, name='user_logout'),
]
