from django.db import models
from django.forms.widgets import Textarea, TextInput
from django.forms import ModelForm
from ckeditor.fields import RichTextField
from base.choices import *

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
    year = models.IntegerField(null=False, blank=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    associated_with = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title

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
    title = models.CharField(max_length=128, null=False, blank=False)
    abstract_text = RichTextField(null=False, blank=False, help_text=ABSTRACT_TEXT_HELP)
    acknowledgements = models.TextField(null=True, blank=True)
    references = models.TextField(null=True, blank=True, help_text=REFERENCES_HELP)
    comments = models.TextField(null=True, blank=True, help_text=COMMENTS_HELP)
    funding = models.NullBooleanField(help_text=FUNDING_HELP)
    year = models.IntegerField(null=False, blank=False)
    last_modified = models.DateField(null=False, blank=True, auto_now_add=True, auto_now=True)
    created = models.DateField(null=False, blank=True, auto_now_add=True)
    abstract_rank = models.IntegerField(null=True, blank=True)
    abstract_media = models.FileField(upload_to="media/", null=True, blank=True)

    def __unicode__(self):
        return self.title[0:20]


class Author(models.Model):
    abstract = models.ForeignKey('Abstract')
    author_rank = models.IntegerField()
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, null=True, blank=True)
    institution = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, choices=COUNTRY_CHOICES)
    email_address = models.EmailField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name


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
