from django.conf.urls import patterns, url
from meetings import views

urlpatterns = patterns('',
                       # ex /meetings/
                       url(r'^$', views.MeetingsView.as_view(), name='meetings'),
                       # ex /meetings/2013/
                       url(r'^(?P<year>\d{4})/$', views.MeetingsDetailView.as_view(), name='meeting_detail'),
                       # ex /meetings/abstract/add/
                       #url(r'^abstract/add/$', views.AbstractCreateView.as_view(), name='create_abstract'),
                       url(r'^abstract/add/$', 'meetings.views.create_abstract', name='create_abstract'),

                       )

