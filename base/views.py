# Create your views here.
# Using class based views.

from django.views import generic
from models import *
from django.core.urlresolvers import reverse, reverse_lazy
from fiber.views import FiberPageMixin
from django.utils import timezone


"""
Using generic class-based views. Generic views are passed to a fiber mixin class
that adds the fiber page content. The fiber page is then inherited by another
class that is called by urls.py

Ex. generic.ListView -> AnnouncementFiberView -> AnnouncementView
"""


########################
## Announcement Views ##
########################

class AnnouncementFiberView(FiberPageMixin, generic.ListView):
    def get_fiber_page_url(self):
        return reverse('base:home')


class AnnouncementView(AnnouncementFiberView):
    template_name = 'base/home.html'
    context_object_name = 'announcement_list'

    def get_queryset(self):
        """Return a list of current announcements"""
        now = timezone.now()
        return Announcement.objects.filter(pub_date__lte=now).filter(expires__gt=now).filter(approved=True).order_by('-pub_date', '-created')


class AnnouncementDetailFiberView(FiberPageMixin, generic.DetailView):
    # A class to combine the context for the fiber page with the general context.
    def get_fiber_page_url(self):
        # reverse lookup to find the fiber page at /home/detail/
        # this requires that there is a matching fiber page.
        # It also requires that there be a base.url that matches the fiber page.
        return reverse('base:announcement_detail_root')  #


class AnnouncementDetailView(AnnouncementDetailFiberView):
    template_name = 'base/detail.html'
    model = Announcement


#####################
## Join Page Views ##
#####################

class JoinIndexView(FiberPageMixin, generic.ListView):
    # A class to combine the context for the fiber page with the general context.
    def get_fiber_page_url(self):
        return reverse('base:join')


class JoinView(JoinIndexView):
    template_name = 'base/join.html'
    context_object_name = 'announcement_list'

    def get_queryset(self):
        """Return a list of current announcements"""
        now = timezone.now()
        return Announcement.objects.filter(pub_date__lte=now).filter(expires__gt=now).filter(approved=True).order_by('-pub_date')


#######################
## Members Page Views ##
#######################

class MembersIndexFiberView(FiberPageMixin, generic.ListView):
    # A class to combine the context for the fiber page with the general context.
    def get_fiber_page_url(self):
        return reverse('base:members')


class MembersIndexView(MembersIndexFiberView):
    template_name = 'base/members.html'
    context_object_name = 'members_list'

    def get_queryset(self):
        if 'query' in self.request.GET:  # check for data
            query = self.request.GET['query']  # if data present get the request
            if query != '':  # Don't do anything if empty query string
                return Member.objects.filter(last_name__icontains=query).order_by('last_name', 'first_name')


class MemberUpdateFiberView(FiberPageMixin, generic.UpdateView):
    def get_fiber_page_url(self):
        return reverse('base:member_update_root')


class MemberUpdateView(MemberUpdateFiberView):
    model = Member
    fields = ['title', 'first_name', 'last_name', 'email_address',
              'address_line1', 'address_line2', 'address_line3', 'city',
              'state_or_province', 'postal_code', 'country']
    template_name = 'base/member_update.html'
