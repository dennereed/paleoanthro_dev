# Create your views here.
# Using class based views.

from django.views import generic
from models import *
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin
from django.utils import timezone
from django.shortcuts import get_object_or_404


class AnnouncementIndexView(FiberPageMixin, generic.ListView):
    # A class to combine the context for the fiber page with the general context.
    def get_fiber_page_url(self):
        return reverse('base:home')


class IndexView(AnnouncementIndexView):
    template_name = 'base/home.html'
    context_object_name = 'announcement_list'

    def get_queryset(self):
        """Return a list of current announcements"""
        now = timezone.now()
        return Announcement.objects.filter(pub_date__lte=now).filter(expires__gt=now).filter(approved=True).order_by('-pub_date')


class AnnouncementDetailView(FiberPageMixin, generic.DetailView):
    # A class to combine the context for the fiber page with the general context.
    def get_fiber_page_url(self):
        # reverse lookup to find the fiber page at /home/detail/
        # this requires that there is a matching fiber page.
        # It also requires that there be a base.url that matches the fiber page.
        return reverse('base:detail_root') #


class DetailView(AnnouncementDetailView):
    template_name = 'base/detail.html'
    model = Announcement


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
