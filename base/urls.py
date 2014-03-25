from django.conf.urls import patterns, url

from base import views

urlpatterns = patterns('',
                       # ex: /home/
                       url(r'^$', views.IndexView.as_view(), name='home'),
                       # ex /home/2/
                       url(r'^detail/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
                       url(r'^detail/$', views.DetailView.as_view(), name='detail_root'),
                       # exL /home/join
                       url(r'^join/$', views.JoinView.as_view(), name='join'),
                       )

