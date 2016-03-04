from rest_framework import serializers
from django_rest_cryptingfields.serializer_fields import CryptingCharField
from .models import Parent

def getParentCharFieldSerializerClass(key_string):
    class ParentCharFieldSerializer(serializers.ModelSerializer):
        class Meta:
            model = Parent
            fields = ('id', 'char_field',)

        char_field = CryptingCharField(key_string = key_string, allow_blank=True)

    return ParentCharFieldSerializer

def getParentCharFieldMaxSixLengthSerializerClass(key_string):
    class ParentCharFieldSerializer(serializers.ModelSerializer):
        class Meta:
            model = Parent
            fields = ('id', 'char_field',)

        char_field = CryptingCharField(key_string = key_string, allow_blank=True, max_length=6)

    return ParentCharFieldSerializer

def getParentCharFieldMinSixLengthSerializerClass(key_string):
    class ParentCharFieldSerializer(serializers.ModelSerializer):
        class Meta:
            model = Parent
            fields = ('id', 'char_field',)

        char_field = CryptingCharField(key_string = key_string, allow_blank=True, min_length=6)

    return ParentCharFieldSerializer
def getParentTextFieldSerializerClass(key_string):
    class ParentTextFieldSerializer(serializers.ModelSerializer):
        class Meta:
            model = Parent
            fields = ('id', 'text_field',)

        text_field = CryptingCharField(key_string = key_string, allow_blank=True)

    return ParentTextFieldSerializer
