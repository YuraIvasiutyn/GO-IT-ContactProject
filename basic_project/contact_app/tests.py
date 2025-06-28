from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Contact
from . import messages


class ContactTests(TestCase):
    def setUp(self):
        """
        Set up a test case by creating a test user and logging them in with the test client.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_add_contact_view(self):
        """
        Test that a contact can be successfully added through the add contact view.

        This test posts valid contact data to the add contact view and checks if
        the response indicates a successful creation (HTTP 302 status code) and
        verifies that the contact is correctly stored in the database with the
        expected attributes and associated with the current user.
        """

        data = {
            'full_name': 'Ivan Ivanov',
            'email': 'ivan@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'st. Shevchenka, Kyiv',
            'birthday': '1990-01-01',
        }
        response = self.client.post(reverse('contact_app:add_contact'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)

        contact = Contact.objects.first()
        self.assertEqual(contact.full_name, data['full_name'])
        self.assertEqual(contact.email, data['email'])
        self.assertEqual(contact.phone, data['phone'])
        self.assertEqual(contact.address, data['address'])
        self.assertEqual(contact.birthday.isoformat(), data['birthday'])
        self.assertEqual(contact.user, self.user)

    def test_add_contact_missing_required_fields(self):
        """
        Tests that the add contact view does not accept requests with missing
        required fields.

        Given a request to add a contact with a missing required field, the
        add contact view should return a 200 response with a form error
        indicating that the field is required.
        """
        data = {
            # 'full_name'
            'email': 'ivan@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'Address',
            'birthday': '1990-01-01',
        }
        response = self.client.post(reverse('contact_app:add_contact'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertEqual(form.errors['full_name'][0], messages.ERROR_FIELD_REQUIRED)

    def test_add_contact_invalid_phone(self):
        """
        Tests that the add contact view does not accept invalid phone numbers.

        Given a request to add a contact with an invalid phone number, the
        add contact view should return a 200 response with an invalid phone
        number error message in the form.
        """
        data = {
            'full_name': 'Ivan Ivanov',
            'email': 'ivan@example.com',
            'phone': '1234567890',
            'address': 'Address',
            'birthday': '1990-01-01',
        }
        response = self.client.post(reverse('contact_app:add_contact'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertEqual(form.errors['phone'][0],
                         messages.INVALID_PHONE_FORMAT)

    def test_pagination_on_main_view(self):
        """
        Test that the main view paginates contacts.

        Creates 16 contacts, requests the main view, checks that the response is
        paginated and contains 10 contacts, and then requests the second page and
        checks that it contains 6 contacts.
        """
        for i in range(16):
            Contact.objects.create(
                user=self.user,
                full_name=f'User {i}',
                email=f'user{i}@example.com',
                phone='+38 (123) 456-78-90',
                address='Address',
                birthday=date(1990, 1, 1)
            )
        response = self.client.get(reverse('contact_app:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['contacts'].paginator.num_pages >= 2)
        self.assertEqual(len(response.context['contacts']), 10)

        response = self.client.get(reverse('contact_app:main') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), 6)

    def test_filter_contacts_by_days_to_birthday(self):
        """
        Test that the main view is filtering contacts by days to birthday.

        Creates a contact with a birthday in 5 days and checks that this contact is
        present in the list of contacts when requesting the main view with
        ?days=7 filter.
        """
        today = date.today()
        soon_birthday = today + timedelta(days=5)
        contact = {
            'user': self.user,
            'full_name': 'Soon Birthday',
            'email': 'soon@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'Address',
            'birthday': date(today.year, soon_birthday.month, soon_birthday.day)
        }
        Contact.objects.create(**contact)

        response = self.client.get(reverse('contact_app:main') + '?days=7')
        self.assertEqual(response.status_code, 200)
        self.assertIn('contacts', response.context)
        self.assertEqual(len(response.context['contacts']), 1)
        self.assertContains(response, contact['full_name'])
        self.assertContains(response, contact['email'])
        self.assertContains(response, contact['phone'])
        self.assertContains(response, contact['address'])

    def test_birthday_cannot_be_in_future(self):
        """
        Test that the add_contact view is preventing birthday dates in the future.

        POST a form with a birthday date in the future and check that the form
        is not valid and that the error message is "Birthday cannot be in the
        future".
        """
        future_date = date.today() + timedelta(days=1)
        data = {
            'full_name': 'Future User',
            'email': 'future@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'Future address',
            'birthday': future_date.isoformat(),
        }
        response = self.client.post(reverse('contact_app:add_contact'), data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('birthday', form.errors)
        self.assertIn('Birthday cannot be in the future', form.errors['birthday'][0])


class ContactViewsTests(TestCase):
    def setUp(self):
        """
        Set up a test case by creating a test user and logging them in with the test client.
        Also creates a contact for this user.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        self.contact = Contact.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone='+38 (123) 456-78-90',
            address='Test address',
            birthday=date(1990, 1, 1)
        )

    def test_main_view(self):
        """
        Test that the main view shows the contacts of the logged in user.

        GET the main view, check that the HTTP response status code is 200,
        check that the response contains the name, email, phone, and address of the
        test contact, and check that the response contains a list of contacts in
        the context.
        """
        response = self.client.get(reverse('contact_app:main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact.full_name)
        self.assertContains(response, self.contact.email)
        self.assertContains(response, self.contact.phone)
        self.assertContains(response, self.contact.address)
        self.assertIn('contacts', response.context)

    def test_search_main_view(self):
        """
        Test that the main view search functionality returns the correct contact.

        Sends a GET request to the main view with a search query for 'Test'.
        Asserts that the response status code is 200 and that the response
        contains the contact with the full name 'Test User'.
        """

        response = self.client.get(reverse('contact_app:main') + '?query=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_add_contact_view(self):
        """
        Test that the add contact view successfully adds a contact to the
        database for the logged in user.

        Posts valid contact data to the add contact view and checks that the
        response status code is 302 and that the contact is correctly stored in
        the database with the expected attributes and associated with the
        current user.
        """
        data = {
            'full_name': 'Ivan Ivanov',
            'email': 'ivan@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'st. Shevchenka, Kyiv',
            'birthday': '1990-01-01',
        }
        response = self.client.post(reverse('contact_app:add_contact'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.filter(user=self.user, full_name=data['full_name'], email=data['email'],
                                                phone=data['phone'], address=data['address'],
                                                birthday=data['birthday']).count(), 1)

    def test_edit_contact_view(self):
        """
        Test that the edit contact view successfully updates a contact in the
        database for the logged in user.

        Posts valid contact data to the edit contact view and checks that the
        response status code is 302 and that the contact is correctly updated in
        the database with the expected attributes and associated with the
        current user.
        """
        url = reverse('contact_app:edit_contact', args=[self.contact.id])
        data = {
            'full_name': 'Updated User',
            'email': 'updated@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'Updated address',
            'birthday': '1995-05-05',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        updated_contact = Contact.objects.get(id=self.contact.id)
        self.assertEqual(updated_contact.full_name, data['full_name'])
        self.assertEqual(updated_contact.email, data['email'])
        self.assertEqual(updated_contact.phone, data['phone'])
        self.assertEqual(updated_contact.address, data['address'])
        self.assertEqual(updated_contact.birthday, date(1995, 5, 5))

    def test_delete_contact_view(self):
        """
        Test that the delete contact view successfully deletes a contact in the
        database for the logged in user.

        GETs the delete contact view and checks that the response status code is
        200 and that the contact's full name is in the content of the response.
        Then, POSTs to the delete contact view and checks that the response
        status code is 302 and that the contact is no longer in the database.
        """
        url = reverse('contact_app:delete_confirm', args=[self.contact.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact.full_name)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())