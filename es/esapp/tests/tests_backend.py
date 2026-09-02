import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Events

class EventAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username='owner', password='testpass123')
        self.other_user = User.objects.create_user(username='other', password='testpass123')
        self.event = Events.objects.create(
            title='Sample Event',
            date='2025-12-31',
            description='Test',
            location='Pakistan',
            category='MEETING',
            status='published',
            user=self.owner
        )
        print("Init Database Models Test")

    def login(self, user):
        self.client.force_login(user)
        print("Login Test")

    def test_list_events(self):
        response = self.client.get(reverse('api_event_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Sample Event')
        print("Test events listings ...")

    def test_create_event_success(self):
        self.login(self.owner)
        payload = {
        'title': 'New Event',
        'date': '2027-12-25',
        'description': 'A new event',
        'location': 'Lahore',
        'category': 'WORKSHOP',
        'status': 'draft'}
        response = self.client.post(
        reverse('api_event_create'),
        data=json.dumps(payload),
        content_type='application/json'
    )
        print("STATUS:", response.status_code)
        print("CONTENT:", response.content)
        self.assertEqual(response.status_code, 201)
        print("Test Events Creation Success")
    
    def test_create_event_missing_title(self):
        self.login(self.owner)
        payload = {'date': '2027-12-25'}
        response = self.client.post(
            reverse('api_event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        print("Test Events Creation Missing title ...")
    def test_create_event_invalid_date(self):
        self.login(self.owner)
        payload = {'title': 'Past Event', 'date': '2020-01-01'}
        response = self.client.post(
            reverse('api_event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        print("Test create invalid date ...")

    def test_create_event_unauthenticated(self):
        payload = {'title': 'Unauth', 'date': '2025-12-25'}
        response = self.client.post(
            reverse('api_event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [302, 403])
        print("Test Events Creation ")

    def test_delete_event_owner(self):
        self.login(self.owner)
        response = self.client.delete(
            reverse('api_event_delete', args=[self.event.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Events.objects.filter(id=self.event.id).exists())
        print("Test Events Creation Success")

    def test_delete_event_non_owner(self):
        self.login(self.other_user)
        response = self.client.delete(
            reverse('api_event_delete', args=[self.event.id])
        )
        self.assertEqual(response.status_code, 403)
        print("Test delete event non owner")

    def test_delete_event_unauthenticated(self):
        response = self.client.delete(
            reverse('api_event_delete', args=[self.event.id])
        )
        self.assertIn(response.status_code, [302, 403])
        print("test delete event unauthenticated")




# Error Life 4 Coders! ^_^

# from django.test import TestCase
# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Events
# import json

# class EventAPITest(TestCase):

#     def setUp(self):
#         self.client = Client()
#         # Create test users
#         self.owner = User.objects.create_user(username='owner', password='testpass123')
#         self.other_user = User.objects.create_user(username='other', password='testpass123')
#         # Create a sample event
#         self.event = Events.objects.create(
#             title='Sample Event',
#             date='2029-12-31',  
#             description='Test description',
#             location='Pakistan',
#             category='MEETING',
#             status='published',
#             user=self.owner
#         )

#     # Helper to log in
#     def login(self, user):
#         self.client.force_login(user)

#     # 1. Happy path: list events
#     def test_list_events(self):
#         response = self.client.get(reverse('event_list_view'))
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertIsInstance(data, list)
#         self.assertEqual(len(data), 1)
#         self.assertEqual(data[0]['title'], 'Sample Event')
#         self.assertEqual(data[0]['id'], self.event.id)

#     # 2. Happy path: create event
#     def test_create_event_success(self):
#         self.login(self.owner)
#         payload = {
#             'title': 'New Event',
#             'date': '2027-12-25',
#             'description': 'A new event',
#             'location': 'Lahore',
#             'category': 'WORKSHOP',
#             'status': 'draft'
#         }
#         response = self.client.post(
#             reverse('event_create'),
#             data=json.dumps(payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 201)  # or 200 if your view returns that
#         self.assertTrue(Events.objects.filter(title='New Event').exists())
#         # Check the created event's user is set correctly
#         new_event = Events.objects.get(title='New Event')
#         self.assertEqual(new_event.user, self.owner)

#     # 3. Failure: create event missing required field (title)
#     def test_create_event_missing_title(self):
#         self.login(self.owner)
#         payload = {
#             'date': '2026-12-25',
#             'description': 'No title',
#             'location': 'Lahore',
#             'category': 'MEETING',
#             'status': 'draft'
#         }
#         response = self.client.post(
#             reverse('event_create'),
#             data=json.dumps(payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertFalse(Events.objects.filter(description='No title').exists())

#     # 4. Failure: create event with past date (validation)
#     def test_create_event_invalid_date(self):
#         self.login(self.owner)
#         payload = {
#             'title': 'Past Event',
#             'date': '2020-01-01',
#             'description': 'Invalid date',
#             'location': 'Lahore',
#             'category': 'MEETING',
#             'status': 'draft'
#         }
#         response = self.client.post(
#             reverse('event_create'),
#             data=json.dumps(payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, 400)
#         self.assertFalse(Events.objects.filter(title='Past Event').exists())

#     # 5. Failure: create event unauthenticated
#     def test_create_event_unauthenticated(self):
#         payload = {'title': 'Unauth Event', 'date': '2025-12-25'}
#         response = self.client.post(
#             reverse('event_create'),
#             data=json.dumps(payload),
#             content_type='application/json'
#         )
#         # Login required should redirect to login (302) or return 403
#         self.assertIn(response.status_code, [302, 403])
#         self.assertFalse(Events.objects.filter(title='Unauth Event').exists())

#     # 6. Happy path: delete event by owner
#     def test_delete_event_owner(self):
#         self.login(self.owner)
#         response = self.client.delete(
#             reverse('event_delete', args=[self.event.id])
#         )
#         self.assertEqual(response.status_code, 200)  # or 204
#         self.assertFalse(Events.objects.filter(id=self.event.id).exists())

#     # 7. Failure: delete event by non-owner
#     def test_delete_event_non_owner(self):
#         self.login(self.other_user)
#         response = self.client.delete(
#             reverse('event_delete', args=[self.event.id])
#         )
#         # Should be forbidden or not found (depending on your view)
#         self.assertIn(response.status_code, [403, 404])
#         self.assertTrue(Events.objects.filter(id=self.event.id).exists())

#     # 8. Failure: delete event unauthenticated
#     def test_delete_event_unauthenticated(self):
#         response = self.client.delete(
#             reverse('event_delete', args=[self.event.id])
#         )
#         self.assertIn(response.status_code, [302, 403])
#         self.assertTrue(Events.objects.filter(id=self.event.id).exists())

