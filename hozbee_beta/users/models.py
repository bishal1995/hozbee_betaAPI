from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import hashlib,time
# Create your models here.

# Adresses
class Address(models.Model):
	address = models.AutoField(primary_key=True,unique=True,db_index=True)
	owner = models.ForeignKey(User)
	service_area = models.ForeignKey('sales.Area',null=True)
	pin = models.CharField(max_length=6)
	building = models.CharField(max_length=10)
	room = models.CharField(max_length=5)


# Customer Group
class CustomerGroup(models.Model):
	group = models.AutoField(primary_key=True,db_index=True)
	group_code = models.CharField(max_length=10)

# Customer details
class CustomerDetails(models.Model):
	customer = models.OneToOneField( User,primary_key=True,db_index=True )
	phone = models.CharField(max_length=10)
	registration_date = models.DateField(auto_now_add=True)
	registration_time = models.TimeField(auto_now_add=True)
	group = models.ForeignKey(CustomerGroup,null=True)

