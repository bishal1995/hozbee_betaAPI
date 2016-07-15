from rest_framework import serializers
from .models import UnitProduct,LaundryCatalogueItem,FoodCategory


class UnitProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = UnitProduct
		fields = ( 'product','product_name','active','available_from','available_to','rating','veg','price','half','half_price','thumbnail' )

class LaundryCatalogueItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = LaundryCatalogueItem
		fields = ( 'cloth','cloth_name','wash_price','washService','clothcategory' )

class FoodCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodCategory
		fields = ( 'category','category_name','parent','level','food' )
		

