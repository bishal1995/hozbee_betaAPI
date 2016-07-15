from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Delivery Boy

class DeliveryBoy(models.Model):
	deliveryboy = models.OneToOneField( User,primary_key=True )
	name = models.CharField(max_length=20)
	
