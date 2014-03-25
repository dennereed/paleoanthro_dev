from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

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

ANNOUNCEMENT_CHOICES = (
    ('Conference', 'Conference'),
    ('Education', 'Education'),
    ('Genera', 'General'),
    ('Job', 'Job'),
)


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    short_title = models.CharField(max_length=50, null=False, blank=False)
    stub = RichTextField()
    body = RichTextField()
    category = models.CharField(max_length=20, choices=ANNOUNCEMENT_CHOICES)
    priority = models.IntegerField()
    created = models.DateField(default=timezone.now())
    pub_date = models.DateField(default=timezone.now())
    expires = models.DateField()
    approved = models.NullBooleanField()

    def __unicode__(self):
        return self.title[0:20]

    def body_header(self):
        return self.body[0:50]

    def is_active(self):
        now = timezone.now()
        return self.expires > now and self.pub_date <= now and self.approved is True
    is_active.admin_order_field='pub_date'
    is_active.boolean = True
    is_active.short_description='Active'