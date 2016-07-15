from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Ratings(models.Model):
	rating = models.AutoField(primary_key=True,db_index=True)
	product = models.ForeignKey('products.UnitProduct')
	customer = models.ForeignKey('users.CustomerDetails')
	rating = models.PositiveSmallIntegerField()
	date = models.DateField()
	time = models.TimeField()

# Reviews
class Reviews(models.Model):
	review = models.AutoField(primary_key=True,db_index=True)
	product = models.ForeignKey('products.UnitProduct')
	customer = models.ForeignKey('users.CustomerDetails')
	review_text = models.TextField()
	date = models.DateField()
	time = models.TimeField()
