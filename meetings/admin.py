from django.contrib import admin
from models import *
from django import forms
from django.forms.widgets import Textarea


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email_address', 'abstract', 'author_rank',)
    list_display_links = ['id', 'name']
    list_filter = ['abstract']
    search_fields = ['id', 'name', 'email_address', 'abstract']


class AuthorInline(admin.TabularInline):
    model = Author


class AbstractAdminForm(forms.ModelForm):
    class Meta:
        model = Abstract
        #widgets = {'title': TextInput(attrs={'size': 120, })}
        widgets = {'title':Textarea(attrs={'cols': 80, 'rows': 2})}


class AbstractAdmin(admin.ModelAdmin):
    list_display = ('id','contact_email', 'presentation_type', 'title', 'year', 'abstract_rank', 'accepted')
    list_display_links = ['id', 'title']
    list_editable = ['accepted', ]
    list_filter = ['year', 'presentation_type', 'abstract_rank', 'accepted']
    search_fields = ['title', 'author__name']
    form = AbstractAdminForm
    inlines = [AuthorInline, ]
    #actions = [create_abstract_csv, create_abstract4meeting_html, create_abstract4publication_html]


class AbstractInline(admin.TabularInline):
    model = Abstract


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'location', 'start_date', 'end_date', 'associated_with')
    list_display_links = ['id', 'location']
    list_editable = []
    list_filter = ['associated_with']
    search_fields = ['location', 'associated_with', 'description']
    inlines = [AbstractInline, ]

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Abstract, AbstractAdmin)
admin.site.register(Author, AuthorAdmin)

