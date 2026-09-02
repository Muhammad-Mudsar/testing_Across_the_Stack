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
            date='2026-12-31',
            description='Test description',
            location='Pakistan',
            category='MEETING',
            status='published',
            user=self.owner
        )

    def login(self, user):
        self.client.force_login(user)

    # 1. List events (JSON)
    def test_list_events(self):
        response = self.client.get(reverse('api_event_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Sample Event')
        self.assertEqual(data[0]['id'], self.event.id)

    # 2. Create event 
    def test_create_event_success(self):
        self.login(self.owner)
        payload = {
            'title': 'New Event',
            'date': '2026-12-25',
            'description': 'A new event',
            'location': 'Lahore',
            'category': 'WORKSHOP',
            'status': 'draft'
        }
        response = self.client.post(
            reverse('event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Events.objects.filter(title='New Event').exists())
        new_event = Events.objects.get(title='New Event')
        self.assertEqual(new_event.user, self.owner)

    # 3. Create event – missing title
    def test_create_event_missing_title(self):
        self.login(self.owner)
        payload = {'date': '2026-12-25'}
        response = self.client.post(
            reverse('event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Events.objects.filter(date='2026-12-25').exists())

    # 4. Create event – invalid date (past)
    def test_create_event_invalid_date(self):
        self.login(self.owner)
        payload = {'title': 'Past Event', 'date': '2020-01-01'}
        response = self.client.post(
            reverse('api_event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Events.objects.filter(title='Past Event').exists())

    # 5. Create event – unauthenticated
    def test_create_event_unauthenticated(self):
        payload = {'title': 'Unauth', 'date': '2025-12-25'}
        response = self.client.post(
            reverse('api_event_create'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [302, 403])
        self.assertFalse(Events.objects.filter(title='Unauth').exists())

    # 6. Delete event – owner
    def test_delete_event_owner(self):
        self.login(self.owner)
        response = self.client.delete(
            reverse('api_event_delete', args=[self.event.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Events.objects.filter(id=self.event.id).exists())

    # 7. Delete event – non-owner
    def test_delete_event_non_owner(self):
        self.login(self.other_user)
        response = self.client.delete(
            reverse('api_event_delete', args=[self.event.id])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Events.objects.filter(id=self.event.id).exists())

    # 8. Delete event – unauthenticated
    def test_delete_event_unauthenticated(self):
        response = self.client.delete(
            reverse('api_event_delete', args=[self.event.id])
        )
        self.assertIn(response.status_code, [302, 403])
        self.assertTrue(Events.objects.filter(id=self.event.id).exists())