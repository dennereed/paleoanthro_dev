from django.views import generic
from models import *
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin


class MeetingsView(FiberPageMixin, generic.ListView):
    # default template name is 'meetings/meeting_list.html'
    model = Meeting

    def get_fiber_page_url(self):
        return reverse('meetings:meetings')


class MeetingsDetailView(FiberPageMixin, generic.DetailView):
    template_name = 'meetings/meeting_detail.html'

    # Define the meeting object
    def get_object(self, queryset=None):
        meeting_year=self.kwargs['year']
        return Meeting.objects.get(year=meeting_year)

    # Fetch corresponding fiber page content
    # In this view there is a separate fiber page for
    # every meeting
    def get_fiber_page_url(self):
        return reverse('meetings:meeting_detail', kwargs={'year': self.kwargs['year']})


