from django.views import generic
from models import *
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin


class MeetingsView(FiberPageMixin, generic.ListView):
    # default template name is 'meetings/meeting_list.html'
    model = Meeting

    def get_fiber_page_url(self):
        return reverse('meetings:meetings')


class MeetingsDetailView(FiberPageMixin, generic.ListView):
    template_name = 'meetings/meeting_detail.html'

    def get_queryset(self):
        # TODO Sort abstracts by lead author last name
        # send a queryset of Authors?
        # convert the queryset object into a list of objects and sort that
        # This needs to be returned in the context not the get_queryset method
        #abstracts = Abstract.objects.select_related().filter(meeting__year__exact=self.kwargs['year'], accepted__exact=True)
        #abstract_list = list(abstracts)
        #abstract_list.sort(key=lambda x: x.author_set.order_by('author_rank')[0].last_name)
        # TODO Add ajax to access absrtact text inline
        return Abstract.objects.select_related().filter(meeting__year__exact=self.kwargs['year'], accepted__exact=True).order_by('title')

    # Fetch corresponding fiber page content
    # In this view there is a separate fiber page for
    # every meeting
    def get_fiber_page_url(self):
        return reverse('meetings:meeting_detail', kwargs={'year': self.kwargs['year']})


#class AbstractForm(FiberPageMixin, generic.ListView):

