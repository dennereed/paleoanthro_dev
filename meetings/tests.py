from django.test import TestCase
from models import Meeting, Abstract, Author
from django.core.urlresolvers import reverse
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


# Factory methods to create test abstracts, meetings, and authors
def create_meeting(year=2020, title='Jamaica 2020', location='Jamaica', associated_with='AAPA'):
    """
    Creates a Meeting with default values for year, title, location and associated_with.
    """
    return Meeting(title, year, location=location,associated_with=associated_with)


def create_three_meetings_with_pages():
    # Create base fiber tree
    create_django_page_tree()
    # Create meeting instances
    calgary = Meeting(year=2014, title='Calgary 2014', location='Calgary', associated_with='AAPA')
    calgary.create_fiber_page()
    calgary.save()
    san_francisco = Meeting(year=2015, title='San Francisco 2015', location='San Francisco', associated_with='SAA')
    san_francisco.create_fiber_page()
    san_francisco.save()
    atlanta = Meeting(year=2016, title='Atlanta 2016', location='Atlanta', associated_with='AAPA')
    atlanta.create_fiber_page()
    atlanta.save()


def create_abstract(meeting,
                    contact_email='denne.reed@gmail.com',
                    presentation_type='Paper',
                    title='Silly Walks of the Neanderthals',
                    abstract_text="""<p> Test abstract text about silly walks in Neanderthals.</p> """,
                    year=2020):

    return Abstract(meeting, contact_email, presentation_type, title, abstract_text, year=year)


def create_author(abstract, author_rank,
                  last_name='Fake',
                  first_name="Ima",
                  name='Ima Fake',
                  department='Entropology',
                  institution='Chaos University',
                  country= 'United States of America',
                  email_address='denne.reed@gmail.com'
                  ):

    return Author(abstract, author_rank,
                  last_name=last_name,
                  first_name=first_name,
                  name=name,
                  department=department,
                  institution=institution,
                  country=country,
                  email_address=email_address
                  )


class MeetingMethodTests(TestCase):
    def test_meeting_create_fiber_page_method(self):
        """
        Tests the fiber page constructor method. The fiber page method get_absolute_url does
        not work as expected. Not sure why....
        """
        # Create a meeting
        calgary_2014 = Meeting(year=2014, title='Calgary 2014', location='Calgary', associated_with='AAPA')
        calgary_2014.save()
        # Create a default page tree
        create_django_page_tree()
        # Call page constructor method
        calgary_2014.create_fiber_page()
        # Fetch the fiber page we just created
        calgary_2014_fiber_page = Page.objects.get(url__exact='2014')
        # Test the attributes of the fiber page
        self.assertEqual(calgary_2014_fiber_page.parent, Page.objects.get(url__exact='meetings'))
        self.assertEqual(calgary_2014_fiber_page.url, '2014')
        self.assertEqual(calgary_2014_fiber_page.title, 'Calgary 2014')
        #self.assertEqual(calgary_2014_fiber_page.get_absolute_url, '/meetings/2014/') TODO Whys does this test fail?
        # Test that the page renders
        response = self.client.get('/meetings/2014/')
        self.assertEqual(response.status_code, 200)

    def test_meeting_has_detail_method(self):
        """
        Tests for the has_detail method
        """
        calgary_2014 = Meeting(year=2014, title='Calgary 2014', location='Calgary', associated_with='AAPA')
        calgary_2014.save()


class MeetingsViewTests(TestCase):
    def test_meetings_index_view_with_no_meetings(self):
        create_django_page_tree()
        response = self.client.get(reverse('meetings:meetings'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['meeting_list'], [])

    def test_meetings_index_view_with_meetings(self):
        create_three_meetings_with_pages()
        response = self.client.get(reverse('meetings:meetings'))
        self.assertContains(response, "Calgary 2014", status_code=200)
        self.assertContains(response, "San Francisco 2015", status_code=200)
        self.assertContains(response, "Atlanta 2016", status_code=200)
        self.assertQuerysetEqual(response.context['meeting_list'], ['<Meeting: Atlanta 2016>', '<Meeting: San Francisco 2015>', '<Meeting: Calgary 2014>'])
        #self.assertContains(response, "<a", status_code=200, html=True)  # contains a table listing meetings

    def test_meetings_index_view_with_missing_meetings(self):
        create_three_meetings_with_pages()
        response = self.client.get(reverse('meetings:meetings'))
        self.assertNotContains(response, "Vancouver", status_code=200)  # Returns page but does not contain a meeting that does not exist.
        #self.assertContains(response, "<table>", status_code=200, html=True)  # contains a table listing meetings




