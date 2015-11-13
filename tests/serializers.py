from rest_framework import serializers
from django_rest_cryptingfields.serializer_fields import CryptingCharField
from .models import Parent

def getParentSerializerClass(key_string):
    class ParentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Parent

        char_field = CryptingCharField(key_string = key_string)

    return ParentSerializer    


