from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django_rest_cryptingfields.models import SignedModel

@python_2_unicode_compatible
class Parent(models.Model):
  char_field = models.CharField(max_length = 1000, default = 'Parent CharField contents.')
  text_field = models.TextField()

  def __str__(self):
    return self.char_field


@python_2_unicode_compatible
class Child(models.Model):
  char_field = models.CharField(max_length=50, default = 'Child CharField contents.', unique=True)
  text_field = models.TextField(default = 'Child TextField contents.')
  decimal_field = models.DecimalField(max_digits=20, decimal_places=3, default=3.434)
  date_field = models.DateTimeField(auto_now_add=True)
  parent = models.ForeignKey('Parent')

  def natural_key(self):
    return (self.char_field)

  def __str__(self):
    return self.char_field

@python_2_unicode_compatible
class SignedParent(SignedModel):
  char_field = models.CharField(max_length = 1000, blank=True, default = '')
  text_field = models.TextField(blank=True, default = '')
  bool_field = models.BooleanField(default = False)
  datetime_field = models.DateTimeField(null=True)
  datetime_field2 = models.DateTimeField(null=True)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.char_field

