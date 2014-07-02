"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from base.models import Member, Announcement, Membership
from fiber.models import Page
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime


# Factory method to create a fiber page tree.
def create_django_page_tree():
    mainmenu=Page(title='mainmenu')
    mainmenu.save()
    home = Page(title='home', parent=mainmenu, url='home', template_name='base/home.html')
    home.save()
    join = Page(title='join', parent=home, url='join', template_name='base/join.html')
    join.save()
    members = Page(title='members', parent=home, url='members', template_name='base/members.html')
    members.save()
    meetings = Page(title='meetings', parent=mainmenu, url='meetings', template_name='')
    meetings.save()


class AnnouncementMethodTests(TestCase):
    def test_create_announcement(self):
        announcements_starting_count = Announcement.objects.count()
        Announcement.objects.create(title="Test Title",
                                    short_title="Test_Short_Title",
                                    body="<p>Announcement body text html format</p>",
                                    category="Job",
                                    priority=1,
                                    expires=timezone.now()+datetime.timedelta(days=1),
                                    approved=True,
                                    )
        announcements_end_count = Announcement.objects.count()
        self.assertEqual(announcements_end_count, announcements_starting_count+1)

    def test_announcements_is_active_method(self):
        announcements_starting_count = Announcement.objects.count()
        Announcement.objects.create(title="Test Active Announcement",
                                    short_title="Test_Short_Title",
                                    body="<p>Announcement body text html format</p>",
                                    category="Job",
                                    priority=1,
                                    expires=timezone.now()+datetime.timedelta(days=1),  # current announcement
                                    approved=True,
                                    )
        Announcement.objects.create(title="Test Expired Announcement",
                                    short_title="Test_Short_Title",
                                    body="<p>Announcement body text html format. To be or not to be that is the"
                                         "question. Whether t'is nobler in the mind to suffer the slings and arrows"
                                         "of outrageous fortune or to take arms against a sea of troubles and by "
                                         "opossing end them.</p>",
                                    category="Job",
                                    priority=1,
                                    expires=timezone.now()+datetime.timedelta(days=-1),  # expired announcement
                                    approved=True,
                                    )
        announcements_end_count = Announcement.objects.count()
        self.assertEqual(announcements_end_count, announcements_starting_count+2)
        announcement = Announcement.objects.get(title="Test Active Announcement")
        self.assertEqual(announcement.pk, 1)
        self.assertEqual(announcement.is_active(), True)  # should be true b/c pub_date current, approved, not expired
        expired_announcement = Announcement.objects.get(title="Test Expired Announcement")
        self.assertEqual(expired_announcement.is_active(), False)  # Should return False

        # create different pub dates
        old_pub_datetime = timezone.now()+datetime.timedelta(days=-2)
        old_pub_date = old_pub_datetime.date()
        future_pub_datetime = timezone.now()+datetime.timedelta(days=+2)
        future_pub_date = future_pub_datetime.date()
        # Test is active method with different pub dates
        announcement.pub_date = old_pub_date  # current announcement has older pub date
        self.assertEqual(announcement.is_active(), True)  # past or current pub date should be active
        announcement.pub_date = future_pub_date
        self.assertEqual(announcement.is_active(), False)  # future pub date should not be active
        announcement.pub_date = old_pub_date
        self.assertEqual(announcement.is_active(), True)  # return to good pub date, should be true
        announcement.approved = False
        self.assertEqual(announcement.is_active(), False)  # OK pub date, but not approved
        # Test body_header method
        self.assertEqual(expired_announcement.body_header(), "<p>Announcement body text html format. To be or no")
        self.assertEqual(len(expired_announcement.body_header()), 50)


class MemberMethodTest(TestCase):

    def test_create_member_method(self):
        m = Member(last_name='Bugglesworth', first_name='Paul', title="Dr.", member=True, registered=False)
        self.assertEqual(m.last_name, 'Bugglesworth')

        member_start_count = Member.objects.count()
        m.save()
        Member.objects.create(last_name="Lennon", first_name="John", member=True, registered=True)
        member_end_count = Member.objects.count()
        self.assertEqual(member_end_count, member_start_count+2)

    def test_uppercase_name_method(self):
        m = Member.objects.create(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.upper_case_name(), 'Paul Bugglesworth')

    def test_uppercase_name_method_with_title(self):
        m = Member(title='Dr.', last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.upper_case_name(), 'Dr. Paul Bugglesworth')

    def test_recent_membership_method(self):
        member_start_count = Member.objects.count()
        membership_start_count = Membership.objects.count()
        member = Member.objects.create(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(member.recent_membership(), 'None')  # None b/c Membership table is empty
        self.assertEqual(member.recent_registration(), 'None')  # because no registration record
        Membership.objects.create(member=member, year=2013, payment_type="M")  # Add a membership record
        self.assertEqual(member.recent_membership(), '2013')  # True now that there is a membership record
        self.assertEqual(member.recent_registration(), 'None')  # because no registration record
        Membership.objects.create(member=member, year=2013, payment_type="R")  # Add a registration record
        self.assertEqual(member.recent_membership(), '2013')
        self.assertEqual(member.recent_registration(), '2013')
        Membership.objects.create(member=member, year=2014, payment_type="M")  # Add a membership record
        self.assertEqual(member.recent_membership(), '2014, 2013')
        self.assertEqual(member.recent_registration(), '2013')

        membership_end_count = Membership.objects.count()
        self.assertEqual(membership_end_count, membership_start_count+3)
        member_end_count = Member.objects.count()
        self.assertEqual(member_end_count, member_start_count+1)


class PageViewTests(TestCase):
    """ test reverse lookups for urls """
    def test_reverse_method_for_home(self):
        self.assertEqual(reverse('base:home'), '/home/')

    def test_reverse_method_for_home_page(self):
        create_django_page_tree()
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 200)

    def test_reverse_method_for_join_page(self):
        create_django_page_tree()
        response = self.client.get(reverse('base:join'))
        self.assertEqual(response.status_code, 200)

    def test_reverse_method_for_members_page(self):
        create_django_page_tree()
        response = self.client.get(reverse('base:members'))
        self.assertEqual(response.status_code, 200)