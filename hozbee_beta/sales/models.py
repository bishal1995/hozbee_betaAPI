from __future__ import unicode_literals

from django.db import models

# Food Orders

# Order Details
class Order(models.Model):
	order = models.AutoField(primary_key=True,db_index=True)
	product = models.ForeignKey('products.UnitProduct')
	quantity = models.PositiveSmallIntegerField()
	price = models.PositiveSmallIntegerField()
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	coupon_applied = models.BooleanField(default=False)
	coupon = models.ForeignKey('products.Coupon',null=True)
	discount_type = models.CharField(max_length=2,null=True)
	discount_figure = models.DecimalField(max_digits=6,decimal_places=2,default=0000.00)
	discount_amount = models.DecimalField(max_digits=6, decimal_places=2,default=0000.00)
	half = models.BooleanField(default=False)
	tax = models.ForeignKey('Tax',null=True)
	tax_percent = models.DecimalField(max_digits=2, decimal_places=2,default=00.00)
	tax_amount = models.DecimalField(max_digits=7, decimal_places=2,default=00000.00)
	status = models.CharField(max_length=2,default='AA')
	total_amount = models.DecimalField(max_digits=7,decimal_places=2)

# Cumulative order
class Corder(models.Model):
	corder = models.AutoField(primary_key=True,db_index=True)
	customer = models.ForeignKey('users.CustomerDetails')
	cart = models.ForeignKey('Cart')
	address = models.ForeignKey('users.Address')
	status = models.CharField(max_length=2,default='AA')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	identifier = models.CharField(max_length=64,default='SOME_UNIQUE_ID')
	total_bill = models.DecimalField(max_digits=7, decimal_places=2)
	shipment = models.OneToOneField('Shipment',null=True)
	invoice = models.OneToOneField('Invoice',null=True)
	transaction = models.OneToOneField('Transaction',null=True)
	payment = models.OneToOneField('Payment',null=True)
	revenuegenerated = models.OneToOneField('RevenueGenerated')
	taxcollection = models.OneToOneField('TaxCollection')


# Cumulative Order Content
class CorderContent(models.Model):
	corder = models.ForeignKey('sales.Corder')
	order = models.OneToOneField('sales.Order')


# Cart
class Cart(models.Model):
	cart = models.AutoField(primary_key=True,db_index=True)
	customer = models.ForeignKey('users.CustomerDetails')
	cart_status = models.CharField(max_length=2,default='AA')  
	date = models.DateField(auto_now=True)
	time = models.TimeField(auto_now=True)
	identifier = models.CharField(max_length=64,default='SOME_UNIQUE_ID')

class CartContent(models.Model):
	cart = models.ForeignKey('Cart')
	product = models.ForeignKey('products.UnitProduct')
	quantity = models.PositiveSmallIntegerField(default=0)
	half = models.CharField(max_length=1,default='0')


## Laundry

# Laundry Corder
class LaundryCorder(models.Model):
	corder = models.AutoField(primary_key=True,db_index=True)
	customer = models.ForeignKey('users.CustomerDetails')
	address = models.ForeignKey('users.Address')
	service = models.CharField(max_length=5,default='0000')
	seller = models.ForeignKey('serviceproviders.SellerDetails',null=True)
	pickup_Date = models.DateField(auto_now_add=False,null=True)
	date = models.DateField(auto_now_add=True)						# Created
	time = models.TimeField(auto_now_add=True)
	status = models.CharField(max_length=2,default='AA')			# Different status
	identifier = models.CharField(max_length=64,default='SOME_UNIQUE_VALUE',null=True)
	shipment = models.OneToOneField('Shipment',null=True)
	invoice = models.OneToOneField('Invoice',null=True)
	transaction = models.OneToOneField('Transaction',null=True)
	payment = models.OneToOneField('Payment',null=True)



# Shipment
class Shipment(models.Model):
	shipment = models.AutoField(primary_key=True,db_index=True)
	address = models.ForeignKey('users.Address')
	delivery_boy = models.ForeignKey('staff.DeliveryBoy')
	status = models.CharField(max_length=2)
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	updated_date = models.DateField(auto_now_add=True)
	updated_time = models.TimeField(auto_now_add=True)
	payment_status = models.CharField(max_length=2)
	payment_mode = models.CharField(max_length=4)
	item_no = models.PositiveSmallIntegerField()
	customer_message = models.TextField()

# Invoice
class Invoice(models.Model):
	invoice = models.AutoField(primary_key=True,db_index=True)
	delivery_address = models.ForeignKey('users.Address')
	customer = models.ForeignKey('users.CustomerDetails')
	customer_name = models.CharField(max_length=20)
	payment = models.ForeignKey('Payment',null=True)
	shipping_charges = models.DecimalField(max_digits=4,decimal_places=2,default=00.00)
	bill = models.DecimalField(max_digits=7, decimal_places=2)
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)

# Transaction Details
class Transaction(models.Model):
	transaction = models.AutoField(primary_key=True,db_index=True)
	customer = models.ForeignKey('users.CustomerDetails')
	transaction_mode = models.CharField(max_length=10)
	transaction_amount = models.DecimalField(max_digits=7, decimal_places=2)
	transaction_signature = models.CharField(max_length=64,default='GENERATED_SIGNATURE')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	status = models.CharField(max_length=2)
	identifier = models.CharField(max_length=64,default='SOME_UNIQUE_ID')

# Payment Details
class Payment(models.Model):
	payment = models.AutoField(primary_key=True,db_index=True)
	customer = models.ForeignKey('users.CustomerDetails')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	transaction = models.ForeignKey('Transaction')
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	payment_mode = models.CharField(max_length=4)
	done_by = models.CharField(max_length=20,default='CUSTOMER')
	recieved_by = models.CharField(max_length=20,default='DELIVERY_BOY')

# Tax Details
class Tax(models.Model):
	tax = models.AutoField(primary_key=True,db_index=True)
	tax_area = models.ForeignKey('Area')
	tax_percent = models.DecimalField(max_digits=5,decimal_places=4)
	tax_type = models.CharField(max_length=10)
	tax_name = models.CharField(max_length=10)

# Revenue
class Revenue(models.Model):
	revenue = models.AutoField(primary_key=True,db_index=True)
	revenue_percentage = models.DecimalField(max_digits=5,decimal_places=4)
	agreement = models.ForeignKey('serviceproviders.Agreement')
	seller = models.ForeignKey('serviceproviders.SellerDetails')

# Area
class Area(models.Model):
	area = models.AutoField(primary_key=True,db_index=True)
	area_name = models.CharField(max_length=10)

# Calculated revenue
class RevenueGenerated(models.Model):
 	revenuegenerated = models.AutoField(primary_key=True,db_index=True)
 	revenue_amount = models.DecimalField(max_digits=6, decimal_places=2)
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	customer = models.ForeignKey('users.CustomerDetails')

#Tax COllected
class TaxCollection(models.Model):
	taxcollection = models.AutoField(primary_key=True,db_index=True)
	tax_amount = models.DecimalField(max_digits=6, decimal_places=2)
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=True)
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	customer = models.ForeignKey('users.CustomerDetails')

'''

# Proposed model for Laundry Order
class Laundryorder(models.Model):
	order = models.AutoField(primary_key=True,db_index=True)
	cloth = models.ForeignKey('products.LaundryCatalogueItem')
	cloth_no = models.PositiveSmallIntegerField()
	price = models.PositiveSmallIntegerField()
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	coupon_applied = models.BooleanField()
	coupon = models.ForeignKey('products.Coupon')
	discount_type = models.CharField(max_length=2)
	discount_figure = models.DecimalField(max_digits=6,decimal_places=2)
	discount_amount = models.DecimalField(max_digits=6, decimal_places=2)
	tax = models.ForeignKey('Tax')
	tax_percent = models.DecimalField(max_digits=2, decimal_places=2)
	tax_amount = models.DecimalField(max_digits=7, decimal_places=2)
	status = models.CharField(max_length=2)
	total_amount = models.DecimalField(max_digits=7, decimal_places=2)	

# Individual Laundry Order

class LaundryCorder(models.Model):
	corder = models.AutoField(primary_key=True,db_index=True)
	customer = models.ForeignKey('users.CustomerDetails')
	address = models.ForeignKey('users.Address')
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	date = models.DateField(auto_now_add=True)
	time = models.TimeField(auto_now_add=False)
	status = models.CharField(max_length=2)
	identifier = models.CharField(max_length=64)
	quantity = models.PositiveSmallIntegerField()
	total_bill = models.DecimalField(max_digits=7, decimal_places=2)
	shipment = models.OneToOneField('Shipment',null=True)
	invoice = models.OneToOneField('Invoice',null=True)
	transaction = models.OneToOneField('Transaction',null=True)
	payment = models.OneToOneField('Payment',null=True)
	revenuegenerated = models.OneToOneField('RevenueGenerated',null=True)
	taxcollection = models.OneToOneField('TaxCollection',null=True)
'''