from django.test import TestCase
from .models import Parent, Child
from django_rest_cryptingfields.serializer_fields import CryptingCharField, Crypter

class CrypterUnitTests(TestCase):
    def setUp(self):
        self.key = Crypter.generate_key_string()
        self.crypter = Crypter(self.key)

    def tearDown(self):
        pass

    def test_crypter(self):
        encryptedText = self.crypter.encrypt("Scooby Doo")
        print(encryptedText)
        decryptedText = self.crypter.decrypt(encryptedText)
        print(decryptedText)

class SerializerFieldUnitTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cryptingcharfield(self):
        pass

