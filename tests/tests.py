from django.test import TestCase
from .models import Parent, Child
from django_rest_cryptingfields.serializer_fields import CryptingCharField, Crypter

class CrypterUnitTests(TestCase):
    def setUp(self):


    def tearDown(self):

    def test_crypting_serializer_field(self):

class SerializerFieldUnitTests(TestCase):
    def setUp(self):

    def tearDown(self):
       self.archiver.destroy()

    def test_crypter(self):


