from django.db import models

# Create your models here.
class Item(models.Model):
  name = models.CharField (max_length=200)
  quantity = models.FloatField ()
  units = models.CharField (max_length=10)
  def __unicode__(self):
    return "%f %s %s"% (self.quantity, self.units, self.name)

class Meal(models.Model):
  name = models.CharField (max_length=200)
  def __unicode__(self):
    return "%s"% (self.name)

class Recipe(models.Model):
  name = models.CharField (max_length=200)
  def __unicode__(self):
    return "%s"% (self.name)
