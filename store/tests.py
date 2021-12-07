from typing import Reversible
from django.http import response
from django.test import TestCase
from django.urls import reverse
from store.models import Album, Artist, Contact, Booking
from store.views import index

# Create your tests here.
#index page 
class IndexPageTestCase(TestCase):
    
    def setUp(self):
        impossible = Album.objects.create(title='Transmission impossible')
        self.album = Album.objects.get(title='Transmission impossible')


    def test_index_page(self):
       # self.assertEqual('a', 'a')
       response = self.client.get(reverse('index'))
       self.assertEqual(response.status_code, 200)

# test that detail page return 200 if the items exist
    def test_detail_page_returns_200(self):
        album_id = self.album.id
        #impossible = Album.objects.create(title='Transmission impossible')
        #album_id = Album.objects.get(title='Transmission impossible').id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)


# test that detail page return 404 if the items exist
    def test_detail_page_returns_404(self):
        album_id = self.album.id + 1
        #impossible = Album.objects.create(title='Transmission impossible')
        #album_id = Album.objects.get(title='Transmission impossible').id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)


# Booking page
class BookingPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name='Fredie', email="fred@queens.forever")
        impossible = Album.objects.create(title='Transmission impossible')
        jounrney = Artist.objects.create(name="journey")
        impossible.artists.objects.get(title='Transmission Impossible')
        impossible.artists.add(jounrney)
        
        self.contact = Contact.objects.get(name="Fredie")
        self.album = Album.objects.get(name="Transmission impossible")

    def test_new_booking_is_registered(self):
        old_bookings= Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name':name,
            'email':email
        })
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings, old_bookings+1)

