from django.conf.urls import patterns, url
from journal import views

urlpatterns = patterns('',
                       # ex /journal/
                       url(r'^$', views.JournalHome.as_view(), name='journal'),
                       # ex /journal/current_volume/
                       #url(r'^current_volume/$', views.JournalCurrent.as_view(), name='current'),
                       # ex /journal/2013/
                       url(r'^(?P<year>\d{4})/$', views.JournalVolumes.as_view(), name='volumes'),

                       # ex /meetings/abstract/add/
                       #url(r'^abstract/add/$', views.AbstractCreateView1.as_view(), name='create_abstract'),
                       #url(r'^abstract/add/$', 'meetings.views.create_abstract', name='create_abstract'),
                       # ex /meetings/abstract/thanks/
                       #url(r'^abstract/thanks/$', views.AbstractThanksView.as_view(), name='thanks'),

                       )