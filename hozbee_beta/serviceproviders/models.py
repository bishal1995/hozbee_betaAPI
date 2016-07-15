from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import hashlib,time



#Seller Details
class SellerDetails(models.Model):
	seller = models.OneToOneField( User,null=True )
	phone = models.CharField(max_length=10)
	registration_date = models.DateField(auto_now_add=True)
	registration_time = models.TimeField(auto_now_add=True)

# Agreement Details
class Agreement(models.Model):
	agreement = models.AutoField(primary_key=True,db_index=True)
	legal_doc = models.CharField(max_length=20)
	seller = models.ForeignKey('SellerDetails')
	agreement_start_date = models.DateField(auto_now_add=True)
	agreement_end_date = models.DateField()

# Added Items
class AddedItems(models.Model):
	product = models.OneToOneField('products.UnitProduct')
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)

# Order Recieved
class RecievedOrder(models.Model):
	order = models.OneToOneField('sales.Order')
	seller = models.ForeignKey('serviceproviders.SellerDetails',null=True)
	product = models.ForeignKey('products.UnitProduct')
	half = models.CharField(max_length=1,default='0')
	quantity = models.PositiveSmallIntegerField()
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	status = models.CharField(max_length=2,default='AA')

'''

# Seller Credentials
class SellerCredentials(models.Model):
	seller = models.OneToOneField('serviceproviders.SellerDetails',primary_key=True)
	username = models.CharField(max_length=50,db_index=True)
	password = models.CharField(max_length=64)

	# saving hashed password
	def save(self, *args, **kwargs):
		raw = str(self.password) + str(time.time())
		self.password = hashlib.sha224(raw).hexdigest()
		super(SellerCredentials, self).save(*args, **kwargs)

'''