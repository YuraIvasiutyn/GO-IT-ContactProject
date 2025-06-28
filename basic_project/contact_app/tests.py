from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Contact

class ContactTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_add_contact_view(self):
        response = self.client.post(reverse('contact_app:add_contact'), {
            'full_name': 'Ivan Ivanov',
            'email': 'ivan@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'st. Shevchenka, Kyiv',
            'birthday': '1990-01-01',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.full_name, 'Ivan Ivanov')
        self.assertEqual(contact.user, self.user)

    def test_add_contact_missing_required_fields(self):
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
        self.assertEqual(form.errors['full_name'][0], 'This field is required')

    def test_add_contact_invalid_phone(self):
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
                         "Phone number must be entered in the format: '+38 (XXX) XXX-XX-XX'. Up to 15 digits allowed.")

    def test_pagination_on_main_view(self):
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
        today = date.today()
        soon_birthday = today + timedelta(days=5)
        Contact.objects.create(
            user=self.user,
            full_name='Soon Birthday',
            email='soon@example.com',
            phone='+38 (123) 456-78-90',
            address='Address',
            birthday=date(today.year, soon_birthday.month, soon_birthday.day)
        )

        response = self.client.get(reverse('contact_app:main') + '?days=7')
        self.assertEqual(response.status_code, 200)
        self.assertIn('contacts', response.context)
        self.assertEqual(len(response.context['contacts']), 1)
        self.assertContains(response, 'Soon Birthday')


class ContactViewsTests(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse('contact_app:main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertIn('contacts', response.context)

    def test_search_main_view(self):
        response = self.client.get(reverse('contact_app:main') + '?query=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_add_contact_view(self):
        data = {
            'full_name': 'Ivan Ivanov',
            'email': 'ivan@example.com',
            'phone': '+38 (123) 456-78-90',
            'address': 'st. Shevchenka, Kyiv',
            'birthday': '1990-01-01',
        }
        response = self.client.post(reverse('contact_app:add_contact'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.filter(user=self.user, full_name='Ivan Ivanov').count(), 1)

    def test_edit_contact_view(self):
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
        self.assertEqual(updated_contact.full_name, 'Updated User')
        self.assertEqual(updated_contact.email, 'updated@example.com')

    def test_delete_contact_view(self):
        url = reverse('contact_app:delete_confirm', args=[self.contact.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact.full_name)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())
