from django.views import generic
from models import Content
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin
#from fiber.models import Page
#from django.shortcuts import render
#from django.http import HttpResponseRedirect
#from django.core.mail import send_mail


class JournalView(FiberPageMixin, generic.ListView):
    # default template name is 'meetings/meeting_list.html'
    model = Content

    def get_fiber_page_url(self):
        return reverse('journal:journal')


