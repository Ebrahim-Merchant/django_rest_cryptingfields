import json
import hmac
import hashlib
import datetime

from django.db import models
from django.core import exceptions
from django.core import serializers
from django.conf import settings

HMAC_KEY_SETTING = 'HMAC_KEY'

class SignedModel(models.Model):

  signature = models.TextField(default='', blank=True)

  class Meta:
    abstract = True

  def save(self, *args, **kwargs):
    self.signature = SignedModel.get_calced_signature(self)
    super(SignedModel, self).save(*args, **kwargs)

  @classmethod
  def from_db(cls, db, field_names, values):
    instance = super(SignedModel, cls).from_db(db, field_names, values)
    calced_signature = cls.get_calced_signature(instance)
    if instance.signature != calced_signature:
      raise exceptions.ValidationError(
        'saved model signature does not equal calculated signature: problem with data integrity'
      )
    return instance



  @staticmethod
  def datetime_converter(o):
    if isinstance(o, datetime.datetime):
      return o.__str__()

  def serialize(self):
    fields = type(self)._meta.get_fields(include_parents=False, include_hidden=False)
    fields_to_serialize = []
    '''
    Fields that take action in field.pre_save() have to be excluded because Django calls
    each field's pre_save() after model.save() and after the pre_save signal and right before
    committing the data to the database (no hook to override). Action is taken on 
    DateTimeField's auto_now_add and auto_now in DateTimeField's pre_save() so exclude 
    these DateTimeFields. 
    '''
    for field in fields:
      if (
          (field.name != 'signature') and
          (not hasattr(field, 'auto_now_add') or field.auto_now_add == False) and 
          (not hasattr(field, 'auto_now') or field.auto_now == False)
      ):
        fields_to_serialize.append(field)
    field_names = [field.name for field in fields_to_serialize]
    '''
    Don't want pk included because for new objects pk will be null before saving. Unfortunately,
    Django's serializers include pk even if it is not included in fields.
    '''
    serialized_python_array = serializers.serialize('python', [self], fields=field_names)
    serialized_python_self = serialized_python_array[0]
    del serialized_python_self['pk']
    return json.dumps(serialized_python_self, default=SignedModel.datetime_converter)

  @staticmethod
  def get_hmac_key():
    return getattr(settings, HMAC_KEY_SETTING)

  @classmethod
  def get_calced_signature(cls, instance):
    return hmac.new(
      cls.get_hmac_key(), 
      msg=instance.serialize(), 
      digestmod=hashlib.sha256
    ).hexdigest()
