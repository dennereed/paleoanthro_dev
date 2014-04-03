from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
                       # ex /meetings/
                       url(r'^$', views.MeetingsView.as_view(), name='meetings'),
                       # ex /meetings/2013/
                       url(r'^(?P<year>\d{4})/$', views.MeetingsDetailView.as_view(), name='meeting_detail'),
                       )

