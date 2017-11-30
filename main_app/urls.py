from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^slack/oauth/$', views.slack_oauth),
    url(r'^atpytu$', views.atpytu)
]