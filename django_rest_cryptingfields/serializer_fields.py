from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    from keyczar import keyczar, keyczart, readers, keyinfo, keys
except ImportError:
    raise ImportError('Requires keyczar, http://www.keyczar.org')

try:
    from rest_framework import serializers
except ImportError:
    raise ImportError('Requires rest_framework, http://www.django-rest-framework.org')



class Crypter(object):
    """A simple wrapper around keyczar Crypter to symmetrically crypt (encrypt/decrypt) using the AES algorithm 
    that uses keyczar's internal key string instead of keyczar's default key file.
    """

    @classmethod
    def generate_key_string():
        return str(keys.AesKey.Generate())

    def __init__(self, key_string):
        key = keys.AesKey.Read(key_string)        
        reader = readers.StaticKeyReader(key, keyinfo.DECRYPT_AND_ENCRYPT)
        self.crypter = keyczar.Crypter(reader)
        
        """
        Internal notes from keyczar source:
        key = keys.AesKey.Generate() #generate returns an AesKey instance
        aes_key_dict = json.loads(str(key)) #key.__str__ returns a json.dump (AesKey object serialized to json-formatted string) Json loads deserializes into a python dict

        aes_key_string = json.dumps(aes_key_dict) #serializes the dict into a string
        key = keys.AesKey.Read(aes_key_string)#Read json.loads a str containing a json document to a python dict then creates an AesKey
        """

    def decrypt(self, value):
        return self.crypter.Decrypt(value)

    def encrypt(self, data):
        return self.crypter.Encrypt(data)

class CryptingCharField(serializers.CharField):
    """A rest_framework serializer field that encrypts text upon deserialization and decrypts upon serialization. 
    """
    def __init__(self, crypter = Crypter, **kwargs):
        super(CryptingCharField, self).__init__(kwargs)
        self.crypter = crypter

    def to_representation(self, value):
        value = self.crypter.decrypt(value)
        return super(CryptingCharField, self).to_representation(value)

    def to_internal_value(self, data):
        value = super(CryptingCharField, self).to_internal_value(data)
        return self.crypter.encrypt(value)
