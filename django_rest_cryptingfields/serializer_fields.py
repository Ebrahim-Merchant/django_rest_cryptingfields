from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import six

try:
    from keyczar import keyczar, keyczart, readers, keyinfo, keys, errors
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
    def generate_key_string(cls):
        return str(keys.AesKey.Generate(size=256))

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
        value = self.crypter.Decrypt(value)
        return value.decode('utf-8')

    def encrypt(self, data):
        if type(data) == six.types.UnicodeType:
            data = data.encode('utf-8')
        return self.crypter.Encrypt(data)

class CryptingCharField(serializers.CharField):
    """A rest_framework serializer field that encrypts text upon deserialization and decrypts upon serialization. 
    """
    def __init__(self, key_string, **kwargs):
        super(CryptingCharField, self).__init__(**kwargs)
        self.crypter = Crypter(key_string)

    def to_representation(self, value):
        if value is not None and len(value) > 0:
            try:
                value = self.crypter.decrypt(value)
            except errors.Base64DecodingError:
                #just return value as-is if it can't be decrypted in case it was set as unencrypted default value.
                pass
        return super(CryptingCharField, self).to_representation(value)

    def to_internal_value(self, data):
        value = super(CryptingCharField, self).to_internal_value(data)
        return self.crypter.encrypt(value)
