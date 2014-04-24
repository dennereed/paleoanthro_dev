from django.forms import ModelForm
from models import Abstract, Author, Meeting
from django.forms.models import inlineformset_factory
from django.forms.widgets import Textarea, TextInput, HiddenInput
from django import forms


# Abstract Model Form
class AbstractForm(ModelForm):
    confirm_email = forms.EmailField(widget=TextInput(attrs={'size': 60}))
    meeting = forms.ModelChoiceField(queryset=Meeting.objects.filter(year__exact=2015), empty_label=None)
    year = forms.IntegerField(widget=HiddenInput, initial=2015)

    class Meta:
        model = Abstract
        fields = (
            'year',
            'meeting',
            'presentation_type',
            'title',
            'abstract_text',
            'acknowledgements',
            'references',
            'funding',
            'comments',
            'contact_email'
        )

        widgets = {
            'contact_email': TextInput(attrs={'size': 60, }),

            'title': Textarea(attrs={'cols': 60, 'rows': 2}),
            'abstract_text': Textarea(attrs={'cols': 60, 'rows': 20}),
            'acknowledgements': Textarea(attrs={'cols': 60, 'rows': 5}),
            'references': Textarea(attrs={'cols': 60, 'rows': 5}),
            'comments': Textarea(attrs={'cols': 60, 'rows': 10}),
        }


# Author Model Form
class AuthorForm(ModelForm):
    class Meta:
        model = Author

        # fields = (
        #     'name',
        #     'department',
        #     'institution',
        #     'country',
        #     'email_address',
        #     )
        #
        # widgets = {
        #     'name': TextInput(attrs={'size': 50}),
        #     'department': TextInput(attrs={'size': 50}),
        #     'institution': TextInput(attrs={'size': 50}),
        #     'email_address': TextInput(attrs={'size': 50}),
        #     }

# generate an inline formset for authors, exclude author rank field,
# which the view will add automatically. Show three blank author forms
# and don't show delete buttons
AuthorInlineFormSet = inlineformset_factory(Abstract, Author,
                                            form=AuthorForm,
                                            extra=3,
                                            exclude=('author_rank',),
                                            can_delete=False,
                                            )

