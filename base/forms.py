# forms.py
from django import forms


class MemberShearchForm(forms.Form):
    query = forms.CharField()