from rest_framework import serializers
from .models import CartContent,Corder,Order,LaundryCorder

class CartContentSerializer(serializers.ModelSerializer):
	class Meta:
		model = CartContent
		fields = ( 'cart','product','quantity' )

class CorderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Corder
		fields = ( 'corder','address','status','date','time','total_bill' )

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ( 'product','quantity','half','status','total_amount' )

class LaundryCorderSerializer(serializers.ModelSerializer):
	class Meta:
		model = LaundryCorder
		fields = ( 'address','service','date','time','status' )



