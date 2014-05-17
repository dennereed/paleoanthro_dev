from django.views import generic
from models import Content
from django.core.urlresolvers import reverse
from fiber.views import FiberPageMixin
#from fiber.models import Page
#from django.shortcuts import render
#from django.http import HttpResponseRedirect
#from django.core.mail import send_mail


class JournalHome(FiberPageMixin, generic.ListView):
    model = Content
    template_name = 'journal/journal_home.html'

    def get_fiber_page_url(self):
        return reverse('journal:journal')


class JournalCurrent(FiberPageMixin, generic.ListView):
    # default template name is 'meetings/meeting_list.html'
    model = Content
    template_name = 'journal/journal_home.html'


    def get_fiber_page_url(self):
        return reverse('journal:journal')


class JournalVolumes(FiberPageMixin, generic.ListView):
    # default template name is 'meetings/meeting_list.html'
    template_name = 'journal/journal.html'
    context_object_name = 'content_list'

    def get_queryset(self):
        queryset = Content.objects.filter(year__exact=self.kwargs['year'])
        return queryset

    def get_context_data(self, **kwargs):
        year = self.kwargs['year']
        context = super(JournalVolumes, self).get_context_data(**kwargs)
        context['abstracts'] = Content.objects.filter(year=year, article_type="Annual Meeting Abstracts").order_by('start_page_n')
        context['articles'] = Content.objects.filter(year=year, article_type="Articles").order_by('start_page_n')
        context['data'] = Content.objects.filter(year=year, article_type="Data").order_by('start_page_n')
        context['reviews'] = Content.objects.filter(year=year, article_type="Reviews").order_by('start_page_n')
        return context

    def get_fiber_page_url(self):
        return reverse('journal:volumes', kwargs={'year':self.kwargs['year']})
