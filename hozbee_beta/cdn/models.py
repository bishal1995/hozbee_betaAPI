from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Content(models.Model):
	content = models.AutoField(primary_key=True,db_index=True)
	product = models.ForeignKey('products.UnitProduct')
	location = models.CharField(max_length=100)