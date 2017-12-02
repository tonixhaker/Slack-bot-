from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^slack/oauth/$', views.slack_oauth),
    url(r'^atpytu$', views.atpytu),
    url(r'^event$', views.event),
    url(r'^messages_details/(?P<pk>\d+)/$', views.MessagesDetail.as_view(), name='messages_details'),
]