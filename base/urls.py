from django.conf.urls import patterns, url
from base import views

urlpatterns = patterns('',
                       # ex: /home/
                       url(r'^$', views.AnnouncementView.as_view(), name='home'),
                       # ex /home/detail/2/
                       url(r'^detail/(?P<pk>\d+)/$', views.AnnouncementDetailView.as_view(), name='announcement_detail'),
                       # ex /home/detail/
                       url(r'^detail/$', views.AnnouncementDetailView.as_view(), name='announcement_detail_root'),
                       # exL /home/join
                       url(r'^join/$', views.JoinView.as_view(), name='join'),
                       # ex /home/membership
                       url(r'^members/$', views.MembersIndexView.as_view(), name='members'),
                       url(r'^members/(?P<pk>\d+)/$', views.MemberUpdateView.as_view(), name='member_update'),
                       url(r'^members/update/$', views.MemberUpdateView.as_view(), name='member_update_root'),
                       )

