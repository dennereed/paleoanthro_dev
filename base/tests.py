"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from base.models import *
from fiber.models import Page


# Factory method to create a fiber page tree.
def create_django_page_tree():
    mainmenu=Page(title='mainmenu')
    mainmenu.save()
    home=Page(title='home', parent=mainmenu, url='home', template_name='base/home.html')
    home.save()
    join=Page(title='join', parent=home, url='join', template_name='base/join.html')
    join.save()
    members=Page(title='members', parent=home, url='members', template_name='base/members')
    members.save()
    meetings = Page(title='meetings', parent=mainmenu, url='meetings', template_name='')
    meetings.save()


class MemberMethodTest(TestCase):

    def test_create_member_method(self):
        m = Member(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.last_name, 'Bugglesworth')

    def test_uppercase_name_method(self):
        m = Member(last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.upper_case_name(), 'Paul Bugglesworth')

    def test_uppercase_name_method_with_title(self):
        m = Member(title='Dr.', last_name='Bugglesworth', first_name='Paul', member=True, registered=False)
        self.assertEqual(m.upper_case_name(), 'Dr. Paul Bugglesworth')


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