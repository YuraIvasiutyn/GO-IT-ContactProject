from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import File


class FileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_file(self):
        test_file = SimpleUploadedFile("testfile.txt", b"file_content")
        file_obj = File.objects.create(
            user=self.user,
            file=test_file,
            category='document'
        )
        self.assertEqual(file_obj.user.username, 'testuser')
        self.assertEqual(file_obj.category, 'document')
        self.assertTrue(file_obj.file.name.endswith("testfile.txt"))
