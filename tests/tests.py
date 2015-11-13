from django.test import TestCase
from .models import Parent, Child
from django_rest_cryptingfields.serializer_fields import CryptingCharField, Crypter
from rest_framework import serializers
from keyczar import errors
from .serializers import getParentSerializerClass
import json
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from .models import Parent


TEXT = 'Permission is hereby granted, free of charge, to any person obtaining a copy' \
           '+of this software and associated documentation files (the "Software"), to deal' \
           '+in the Software without restriction, including without limitation the rights' \
           '+to use, copy, modify, merge, publish, distribute, sublicense, and/or sell' \
           '+copies of the Software, and to permit persons to whom the Software is' \
           '+furnished to do so, subject to the following conditions:'

class CrypterUnitTests(TestCase):
    def setUp(self):
        self.key = Crypter.generate_key_string()
        self.crypter = Crypter(self.key)

    def tearDown(self):
        pass

    def test_crypting(self):
        encryptedText = self.crypter.encrypt(TEXT)
        decryptedText = self.crypter.decrypt(encryptedText)
        self.assertEqual(decryptedText, TEXT)
        self.assertNotEqual(encryptedText, TEXT)

    def test_key_not_found(self):
        other_key = Crypter.generate_key_string()
        other_crypter = Crypter(other_key)
        encryptedText = self.crypter.encrypt(TEXT)
        encryptedTextOther = other_crypter.encrypt(TEXT)
        self.assertEqual(self.crypter.decrypt(encryptedText), TEXT)
        self.assertEqual(other_crypter.decrypt(encryptedTextOther), TEXT)

        self.assertRaises(errors.KeyNotFoundError, self.crypter.decrypt, encryptedTextOther)

class SerializerFieldUnitTests(TestCase):
    def setUp(self):
        self.key_string = Crypter.generate_key_string()

    def tearDown(self):
        pass

    def test_cryptingcharfield(self):
        json_string = json.dumps({'char_field': TEXT})
        stream = BytesIO(json_string)
        data = JSONParser().parse(stream)        
        deserializer = getParentSerializerClass(self.key_string)(data=data)
        deserializer.is_valid()
        deserializer.save()

        parent_model_from_db = Parent.objects.get(pk=1)        
        parent_model_char_field_from_db = parent_model_from_db.char_field
        self.assertNotEqual(parent_model_char_field_from_db, TEXT)

        serializer = getParentSerializerClass(self.key_string)(parent_model_from_db)
        data = serializer.data
        del data['id']
        serialized_model = JSONRenderer().render(data)
        serialized_model = json.dumps(json.loads(serialized_model)) #get rid of space due to differences in parser output....
        self.assertEqual(serialized_model, json_string)        
        
