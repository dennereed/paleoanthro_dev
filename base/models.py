from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
import os
from choices import COUNTRY_CHOICES, PAYMENT_TYPE_CHOICES, ANNOUNCEMENT_CHOICES
from django.forms import ModelForm
from django.core.urlresolvers import reverse


############################################
# PaleoanthroUser
############################################

class PaleoanthroUser(models.Model):
    """
    This class "extends" the default Django user class. It adds Paleocore
    specific fields to the user database, allowing us to use the auth
    system to track and manage paleocore users rather than constructing a separate
    membership database.

    This class is coupled with a custom PaleoCoreUserAdmin module in base.admin.py
    """
    user = models.OneToOneField(User)

    # other fields
    institution = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    send_emails = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        db_table = "paleoanthro_user"
        verbose_name_plural = "User Info"
        verbose_name = "User Info"
        ordering= ["user__last_name",]


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    short_title = models.CharField(max_length=50, null=False, blank=False)
    stub = RichTextField()
    body = RichTextField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=ANNOUNCEMENT_CHOICES)
    priority = models.IntegerField()
    created = models.DateField(default=timezone.now())
    pub_date = models.DateField(default=timezone.now())
    expires = models.DateField()
    approved = models.NullBooleanField()
    upload1 = models.FileField(upload_to='static/uploads', null=True, blank=True)
    upload2 = models.FileField(upload_to='static/uploads', null=True, blank=True)
    upload3 = models.FileField(upload_to='static/uploads', null=True, blank=True)

    def __unicode__(self):
        return self.title[0:20]

    def body_header(self):
        return self.body[0:50]

    def is_active(self):
        now = timezone.now().date()
        return self.expires > now and self.pub_date <= now and self.approved is True
    is_active.admin_order_field='pub_date'
    is_active.boolean = True
    is_active.short_description='Active'

    def get_absolute_url(self):
        return reverse('announcement_detail', kwargs={'pk':self.id})

    @property
    def upload1_filename(self):
        return os.path.basename(self.upload1.name)

    def upload2_filename(self):
        return os.path.basename(self.upload2.name)

    def upload3_filename(self):
        return os.path.basename(self.upload3.name)


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, null=True, blank=True, help_text="e.g. Mr. Dr., Prof. etc.")
    first_name = models.CharField(max_length=128, null=True, blank=True, help_text="Given name or names")
    last_name = models.CharField(max_length=128, null=True, blank=True,help_text="Family name")
    address_line1 = models.CharField(max_length=128, null=True, blank=True)
    address_line2 = models.CharField(max_length=128, null=True, blank=True)
    address_line3 = models.CharField(max_length=128, null=True, blank=True)
    address_line4 = models.CharField(max_length=128, null=True, blank=True)
    address_line5 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state_or_province = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True, choices=COUNTRY_CHOICES)
    postal_code = models.CharField(max_length=128, null=True, blank=True)
    email_address = models.EmailField(max_length=128, null=True, blank=True)
    old_email_address = models.EmailField(max_length=128, null=True, blank=True)
    hash = models.CharField(max_length=100, null=True, blank=True)
    member = models.NullBooleanField()
    registered = models.NullBooleanField()
    last_modified = models.DateField(auto_now_add=True,auto_now=True, null=False)
    created = models.DateField(auto_now_add=True, null=False)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def upper_case_name(self):
        if self.title:
            return ("%s %s %s" % (self.title, self.first_name, self.last_name)).title()
        else:
            return ("%s %s" % (self.first_name, self.last_name)).title()

        upper_case_name.short_description = 'Name'
        upper_case_name.admin_order_field = 'last_name'

    def is_current_member(self):
        membership_years = self.membership_set.filter(payment_type = 'M').filter(year = 2013)

    def recent_membership(self): # returns the last two years of recorded membership
        membership_objects = self.membership_set.filter(payment_type = 'M')
        membership_years = []
        for o in membership_objects:
            membership_years.append(o.year)
        if membership_years:
            membership_years.sort()
            membership_years.reverse() # most recent years first
            return str(membership_years[:2]).strip('[]') # converts integers to strings and removes braces
        else:
            return 'None'

    def recent_registration(self): # returns the last two years of recorded registration
        registration_objects = self.membership_set.filter(payment_type = 'R')
        registration_years = []
        for o in registration_objects:
            registration_years.append(o.year)
        if registration_years:
            registration_years.sort()
            registration_years.reverse() # most recent years first
            return str(registration_years[:2]).strip('[]') # converts integers to strings and removes braces
        else:
            return 'None'

    def get_absolute_url(self):
        return reverse('base:member_update', kwargs={'pk':self.pk})


class Membership(models.Model):
    member = models.ForeignKey(Member) # the member id
    year = models.IntegerField() # the membership/registration year
    payment_type = models.CharField(max_length=128, choices=PAYMENT_TYPE_CHOICES) # whether the payment is for registration or membership

    def __unicode(self):
        return self.year


### Model Forms ###
class MemberForm(ModelForm):
    class Meta:
        model = Member