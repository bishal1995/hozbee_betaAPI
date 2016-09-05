from __future__ import unicode_literals

from django.db import models

# Abstract Product class
class UnitProduct(models.Model):
	product = models.AutoField(primary_key=True,db_index=True)
	product_name = models.CharField(max_length=20)
	service_area = models.ForeignKey('sales.Area')
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	active = models.BooleanField(default=True)
	available_from = models.TimeField()
	available_to = models.TimeField()
	delivery = models.PositiveSmallIntegerField()				# Minimum delivery time
	rating = models.PositiveSmallIntegerField(default=0)
	veg = models.BooleanField()
	price = models.PositiveSmallIntegerField()
	half = models.BooleanField()								# available as half
	half_price = models.PositiveSmallIntegerField()
	thumbnail = models.URLField(max_length=200)
	tax_id = models.ForeignKey('sales.Tax')
	revenue_id = models.ForeignKey('sales.Revenue')

# Food Category
class FoodCategory(models.Model):
	category = models.AutoField(primary_key=True,db_index=True)
	category_id = models.SmallIntegerField(null=True)
	service_area = models.ForeignKey('sales.Area',null=True)
	category_name = models.CharField(max_length=15)
	food = models.ForeignKey('UnitProduct')

# Product - Bundle Product
class BundleProduct(models.Model):
	products = models.ForeignKey('UnitProduct',primary_key=True,db_index=True)
	minimun_quantity = models.PositiveSmallIntegerField()				# Minimum delivery time
	thumbnail = models.URLField(max_length=200)

# Food Tags
class FoodTags(models.Model):
	tag = models.AutoField(primary_key=True,db_index=True)
	tag_title = models.CharField(max_length=15)

# Tag relations
class TagRelations(models.Model):
	product = models.ForeignKey('UnitProduct',null=True)
	tag = models.ForeignKey('FoodTags',null=True)

	class Meta:
		index_together = ["product", "tag"]

# Laundry Catalogue
class LaundryCatalogueItem(models.Model):
	cloth = models.AutoField(primary_key=True,db_index=True)
	seller = models.ForeignKey('serviceproviders.SellerDetails')
	service_area = models.ForeignKey('sales.Area',null=True)
	cloth_name = models.CharField(max_length=15)
	wash_price = models.PositiveSmallIntegerField()
	WASH_AND_DRY = 'WD'
	WASH_AND_IRON = 'WI'
	DRY_WASH = 'DW'
	WASH_SERVICE_CHOICES = (
		(WASH_AND_DRY, 'WASH_AND_DRY'),
		(WASH_AND_IRON, 'WASH_AND_IRON'),
		(DRY_WASH, 'DRY_WASH'),
    )
	washService = models.CharField(
        max_length=2,
        choices=WASH_SERVICE_CHOICES,
    )
	MALE = 'M'
	FEMALE = 'F'
	HOUSEHOLD = 'H'
	CLOTH_CHOICES = (
		(MALE,'MALE'),
		(FEMALE,'FEMALE'),
		(HOUSEHOLD,'HOUSEHOLD'),
    )
	clothcategory = models.CharField(
        max_length=1,
        choices=CLOTH_CHOICES,
    )


# Coupond
class Coupon(models.Model):
	counpon = models.AutoField(primary_key=True)
	counpon_code = models.CharField(db_index=True,unique=True,max_length=10)
	discount = models.DecimalField(max_digits=6,decimal_places=2)
	validity = models.DateField()
	active = models.BooleanField(default=False)
	DIRECT_DISCOUNT = 'DD'
	PERCENTAGE_DISCOUNT = 'PD'
	DISCOUNT_TYPE_CHOICES = (
		(DIRECT_DISCOUNT,'DIRECT_DISCOUNT'),
		(PERCENTAGE_DISCOUNT,'PERCENTAGE_DISCOUNT'),
    )
	discount_type = models.CharField(
			max_length = 2,
			choices = DISCOUNT_TYPE_CHOICES,
		)

# Applicability
class CouponApplicability(models.Model):
	coupon = models.ForeignKey('Coupon')
	product = models.ForeignKey('UnitProduct')
	active = models.BooleanField(default=False)

	class Meta:
		index_together = ["coupon", "product"]

