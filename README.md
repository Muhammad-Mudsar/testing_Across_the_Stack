# testing_Across_the_Stack

Testing Across the Stack, application actually works with automated tests both on frontend and backend

# complete event Scheduler app + Testing

# Project Documentation: Testing APP

This document explains how to run and extend the automated tests for the application.

## Test Overview

The project includes two main test suites:

- **Backend tests** – verify API endpoints, authentication, and data handling using Django's built-in `TestCase` and `Client`.
- **Frontend tests** – verify server‑rendered HTML pages (forms, validation, page rendering) using Django's test client and BeautifulSoup.

The tests are located in the `esapp/tests/` directory.

## Prerequisites

Ensure you have the required Python packages installed:

```bash
pip install requirements.txt
Django's test runner is included for backend testing.
BeautifulSoup is used only for frontend HTML parsing.

# Running the Tests

python manage.py test esapp.tests.tests_backend

python manage.py test esapp.tests.test_frontend

Run all tests

python manage.py test
Run only backend tests

python manage.py test esapp.tests.test_api
Run only frontend tests
bash
python manage.py test esapp.tests.test_frontend
Run a specific test class or method
bash
python manage.py test esapp.tests.test_api.EventAPITest
python manage.py test esapp.tests.test_frontend.FrontendRenderingTests.test_create_event_success
Backend Tests
File: esapp/tests/test_api.py

These tests cover the API endpoints that return JSON responses. They use Django's Client and TestCase to simulate HTTP requests and verify the response status, JSON structure, and database changes.

What is tested
api_event_list – GET request returns a list of events.

api_event_create – POST with valid data creates an event; missing fields return 400; invalid date returns 400; unauthenticated request is rejected.

api_event_delete – DELETE by owner succeeds; non‑owner is forbidden; unauthenticated is rejected.

Example test
python
def test_create_event_success(self):
    self.login(self.owner)
    payload = {'title': 'New Event', 'date': '2025-12-25'}
    response = self.client.post(reverse('api_event_create'), data=json.dumps(payload), content_type='application/json')
    self.assertEqual(response.status_code, 201)
    self.assertTrue(Events.objects.filter(title='New Event').exists())
Frontend Tests
File: esapp/tests/test_frontend.py

These tests verify that the server‑rendered HTML pages contain the expected form elements, that form validation works correctly, and that successful submissions update the database.

They use Django's Client to make requests and BeautifulSoup to parse the HTML response.

What is tested
Login page renders username, password fields, and submit button.

Successful login redirects away from the login page.

Event creation page renders title, date, description fields.

Submitting valid event data creates the event in the database.

Submitting empty title re‑renders the form with an error message.

Events page loads successfully (even if the list is populated by JavaScript after page load).

Example test
python
def test_create_event_validation_error(self):
    post_data = {'title': '', 'date': '2027-12-31', 'description': 'No title'}
    response = self.client.post(reverse('create'), post_data)
    self.assertEqual(response.status_code, 200)
    self.assertFormError(response, 'form', 'title', 'Title is required')
Note: If the actual error message or form field names differ in your templates, adjust the test assertions accordingly (e.g., 'This field is required.' instead of 'Title is required').

# Test Structure

esapp/
├── tests/
│   ├── __init__.py
│   ├── test_api.py          # Backend API tests
│   └── test_frontend.py     # Frontend rendering/validation tests
Important Notes
The frontend tests assume the HTML forms use the field names title, date, description, etc. If your form uses different names, update the test data.

All tests run against a temporary test database that is created and destroyed automatically by Django.

CSRF protection is disabled by default in Django's test client (enforce_csrf_checks=False), so you don't need to handle CSRF tokens in these tests.

If you later add browser‑based end‑to‑end tests (e.g., with Selenium or Cypress), create a separate test file and document it here.

Extending the Tests
To add a new backend test, open test_api.py and write a method inside EventAPITest.
To add a new frontend test, open test_frontend.py and write a method inside FrontendRenderingTests.

Always follow the pattern:

Use self.client to make requests.

Assert on response.status_code, response.json(), or parsed HTML content.

Use reverse('url_name') instead of hard‑coded URLs.
```
