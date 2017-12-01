from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^slack/oauth/$', views.slack_oauth),
    url(r'^atpytu$', views.atpytu),
    url(r'^test/$', views.testsend),
    url(r'^direct/$', views.testdirect),
    url(r'^event/$', views.event),
]