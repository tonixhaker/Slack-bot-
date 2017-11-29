from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^slack/oauth/$', views.slack_oauth),
    url(r'^atpytu$', views.atpytu)
]