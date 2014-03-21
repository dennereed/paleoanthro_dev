from django.conf.urls import patterns, url

from base import views

urlpatterns = patterns('',
                       # ex: /home/
                       url(r'^$', views.IndexView.as_view(), name='home'),
                       )

