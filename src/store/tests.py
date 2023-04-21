from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Contact, Booking

# Create your tests here.

# Index page
    # Test that index page returns a status code 200
    # Test that index page returns the correct content
# class IndexPageTestCase(TestCase):
#     def test_index_page(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'store/index.html')

class IndexPageTestCase(TestCase):
    # test that index page returns a status code 200
    def test_index_page(self):
        #self.assertEqual("a", "a")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


# Detail page
# class DetailPageTestCase(TestCase):
#     def test_detail_page_returns_200(self):
#         album = Album.objects.create(title="Mon titre", inventory=10, price=10)
#         response = self.client.get(reverse('store:detail', args=(album.id,)))
#         self.assertEqual(response.status_code, 200)
    
#     def test_detail_page_returns_404(self):
#         response = self.client.get(reverse('store:detail', args=(1,)))
#         self.assertEqual(response.status_code, 404)

# # Detail page
#     # Test that detail page returns a status code 200 if the item exists
#     # Test that detail page returns a status code 404 if the item does not exist
# class DetailPageTestCase(TestCase):
#     def test_detail_page_returns_200(self):
#         album = Album.objects.create(title="Mon titre", inventory=10, price=10)
#         response = self.client.get('/store/1/')
#         self.assertEqual(response.status_code, 200)
    
#     def test_detail_page_returns_404(self):
#         response = self.client.get('/store/1/')
#         self.assertEqual(response.status_code, 404)


class DetailPageTestCase(TestCase):

    # Create an album before each test
    def setUp(self):
        new_album =  Album.objects.create(title="Fearless Motivation")
        self.album = Album.objects.get(title="Fearless Motivation")

    # Test that detail page returns a status code 200 if the item exists
    def test_detail_page_returns_200(self):
        # new_album = Album.objects.create(title="Fearless Motivation")
        # album_id = new_album.id
        # album_id = Album.objects.get(title="Fearless Motivation").id
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    
    # Test that detail page returns a status code 404 if the item does not exist
    def test_detail_page_returns_404(self):
        # new_album = Album.objects.create(title="Fearless Motivation")
        # album_id = Album.objects.get(title="Fearless Motivation").id + 1
        album_id = self.album.id + 1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)




# # Booking page
#     # Test that a new booking is made
#     # Test that a booking belongs to a contact
#     # Test that a booking belongs to an album
# class BookingPageTestCase(TestCase):
#     def setUp(self):
#         Contact.objects.create(name="Freddie", email="freddie@example.com")
#         Album.objects.create(title="Mon titre", inventory=10, price=10)
#     def test_new_booking_is_registered(self):
#         # Make a new booking
#         self.client.post(reverse('store:detail', args=(1,)), {
#             'email': 'freddie@example.com'
#         })
#         # Test there is one booking in the database
#         self.assertEqual(Booking.objects.count(), 1)
#         # Test that the album is not available anymore
#         album = Album.objects.get(pk=1)
#         self.assertEqual(album.available, False)
#     def test_new_booking_belongs_to_a_contact(self):
#         # Make a new booking
#         self.client.post(reverse('store:detail', args=(1,)), {
#             'email': 'freddie@example.com'
#         })
#         # Test that the booking is linked to the contact
#         booking = Booking.objects.get(pk=1)
#         contact = Contact.objects.get(pk=1)
#         self.assertEqual(booking.contact, contact)
#     def test_new_booking_belongs_to_an_album(self):
#         # Make a new booking
#         self.client.post(reverse('store:detail', args=(1,)), {
#             'email': 'Freddie@example.com'
#         }) 
#         # Test that the booking is linked to the album
#         booking = Booking.objects.get(pk=1)
#         album = Album.objects.get(pk=1)
#         self.assertEqual(booking.album, album)
#     def test_detail_page_returns_404(self):
#         response = self.client.get('/store/1/')
#         self.assertEqual(response.status_code, 404)

# Booking page
# Nous allons vérifier que : 
# - une nouvelle réservation est bien enregistrée dans la base de données si le formulaire est envoyé est valide
# Pour tester cela, nous allons utiliser la méthode post() de la classe TestCase pour envoyer le formulaire via une requête POST avec les données du formulaire (email, name, etc.) sur la vue détail ( la page de détail d'un album).
class BookingPageTestCase(TestCase):
    # Create an album and a contact before each test
    def setUp(self):
        Contact.objects.create(name="Freddie", email="fred@queens.forever")
        impossible = Album.objects.create(title="Transmission Impossible")
        journey = Artist.objects.create(name="Journey")
        impossible.artists.add(journey)
        self.album = Album.objects.get(title="Transmission Impossible")
        self.contact = Contact.objects.get(name="Freddie")

    # Test that a new booking is made
    def test_new_booking_is_registered(self):
        old_bookings_count = Booking.objects.count()
        # Make a new booking
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(album_id,)), {
            'name': name,
            'email': email,
        })
        new_bookings_count = Booking.objects.count()
        self.assertEqual(new_bookings_count, old_bookings_count + 1)
