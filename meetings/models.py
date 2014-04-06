from django.db import models
from django.forms.widgets import Textarea, TextInput
from django.forms import ModelForm
from ckeditor.fields import RichTextField
from base.choices import *
from fiber.models import Page
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

# Create your models here.

PRESENTATION_TYPE_CHOICES = (
    ('Paper', 'Paper'),
    ('Poster', 'Poster'),
)
FUNDING_CHOICES = (
    ('True','Yes'),
    ('False','No'),
)


class Meeting(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    # year is being used informally as a foreign key to the corresponding fiber page.
    year = models.IntegerField(null=False, blank=False, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    associated_with = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    program_pdf = models.FileField(upload_to='uploads/files', null=True, blank=True)
    abstracts_pdf = models.FileField(upload_to='uploads/files', null=True, blank=True)

    def __unicode__(self):
        return self.title

    # Function used by meetings.html template to test if a meeting page
    # exists and is public. We set the is_public option to True in admin if
    # they contain
    # meeting details. A link to the page is automatically included in meetings.html
    def has_detail(self):
        try:
            p=Page.objects.get(title=self.title)
        # if it doesn't exist, create a new page
        except ObjectDoesNotExist: # it not there create it
            return False
            # Create page if it doesn't exist?
            #p = Page(title=self.title, parent=meetings_page, url=self.year)
            #p.save()
        else:
            if p.is_public:
                return True
            else:
                return False


    def create_fiber_page(self):
        # A method to automatically build the necessary blank fiber page for a meeting instance
        # Requires that a meetings page exists. Meeting detail pages are
        # created under the meetings page
        meetings_page = Page.objects.get(title="meetings")
        # test if a meeting detail page already exists
        try:
            Page.objects.get(title=self.title)
        # if it doesn't exist, create a new page
        except ObjectDoesNotExist: # it not there create it
            p = Page(title=self.title, parent=meetings_page, url=self.year)
            p.save()
        else:
            print("Page already exists")


    # TODO Add is_current method to identify which meeting is the current meeting for the year.

# Variable assignments for Abstract model #

PRESENTATION_TYPE_HELP = "(Please evaluate your material carefully and decide whether a " \
                          "paper or poster is most appropriate. Papers and posters are " \
                          "presented in separate, non-concurrent sessions.)"
ABSTRACT_TEXT_HELP = "(Abstracts are limited to 300 words not counting acknowledgements. They must be in English.)"
REFERENCES_HELP = "(Include references only if they are cited in your abstract. Please follow the " \
                  "<a href='/static/pdfs/PaleoAnthropology%20Guidelines_articles.pdf'>journal&apos;s </a>format)"
COMMENTS_HELP = "(Please include any factors that should be included in an evaluation of this abstract. " \
                "For instance, if this paper is not substantially different from a recently given paper it may " \
                "be rejected. Thus, you might want to make clear how this paper differs.)"
FUNDING_HELP = "Check this box if you would like to be considered for partial funding."


class Abstract(models.Model):
    meeting = models.ForeignKey('Meeting')
    contact_email = models.EmailField(max_length=128, null=False, blank=False)
    presentation_type = models.CharField(max_length=20, null=False, blank=False, choices=PRESENTATION_TYPE_CHOICES,
                                         help_text=PRESENTATION_TYPE_HELP)
    title = models.CharField(max_length=200, null=False, blank=False)
    abstract_text = RichTextField(null=False, blank=False, help_text=ABSTRACT_TEXT_HELP)
    acknowledgements = models.TextField(null=True, blank=True)
    references = models.TextField(null=True, blank=True, help_text=REFERENCES_HELP)
    comments = models.TextField(null=True, blank=True, help_text=COMMENTS_HELP)
    funding = models.NullBooleanField(help_text=FUNDING_HELP)
    year = models.IntegerField(null=False, blank=False)
    last_modified = models.DateField(null=False, blank=True, auto_now_add=True, auto_now=True)
    created = models.DateField(null=False, blank=True, auto_now_add=True)
    abstract_rank = models.IntegerField(null=True, blank=True)
    abstract_media = models.FileField(upload_to="meetings/files", null=True, blank=True)
    accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title[0:20]

    def lead_author_last_name(self):
        return self.author_set.order_by('author_rank')[0].last_name

        lead_author_last_name.short_description = 'Lead Name'



class Author(models.Model):
    abstract = models.ForeignKey('Abstract')
    author_rank = models.IntegerField()
    last_name = models.CharField(null=True, blank=True, max_length=200)
    first_name = models.CharField(null=True, blank=True, max_length=200)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, null=True, blank=True)
    institution = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, choices=COUNTRY_CHOICES)
    email_address = models.EmailField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def full_name(self):
        if self.first_name and self.last_name:
            return ("%s %s" % (self.first_name, self.last_name)).title()
        else:
            raise ObjectDoesNotExist

        full_name.short_description = 'Name'
        full_name.admin_order_field = 'last_name'

    class Meta:
        ordering = ['author_rank']


### Model Forms ###


class AbstractForm(ModelForm):
    class Meta:
        model = Abstract

        fields = (
            'contact_email',
            'presentation_type',
            'title',
            'abstract_text',
            'acknowledgements',
            'references',
            'comments',
            'funding',
        )

        widgets = {
            'contact_email':TextInput(attrs={'size': 40,}),
            'title':TextInput(attrs={'size': 80,}),
            'abstract_text':Textarea(attrs={'cols': 60, 'rows': 20}),
            'acknowledgements':Textarea(attrs={'cols': 60, 'rows': 5}),
            'references':Textarea(attrs={'cols': 60, 'rows': 5}),
            'comments':Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class AuthorForm(ModelForm):
    class Meta:
        model = Author

        fields = (
            'name',
            'department',
            'institution',
            'country',
            'email_address',
        )

        widgets = {
            'name':TextInput(attrs={'size':50}),
            'department':TextInput(attrs={'size':50}),
            'institution':TextInput(attrs={'size':50}),
            'email_address':TextInput(attrs={'size':50}),
        }
