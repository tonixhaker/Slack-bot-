from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='index'),
    url(r'^registration/$', views.RegisterView.as_view(), name='registration'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^auth/$', views.auth_user_try, name='auth'),
]