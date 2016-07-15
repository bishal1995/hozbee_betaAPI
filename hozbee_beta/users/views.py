from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.contrib.auth.models import User
from .models import Address,CustomerDetails

class AddUser(APIView):

	def put(self,request,format=None):
		data = request.body
		data = json.loads(data)
		User.objects.create_user(
			username = data['username'],
			password = data['password'],
			email = data['email']
		).save()
		print(data['username'])
		content={'ok':'value'}
		return Response(content,status=200)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(AddUser, self).dispatch(*args, **kwargs)


class AddAddress(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def put(self,request,format=None):
		data = request.body
		data = json.loads(data)
		address = Address()
		address.owner = request.user
		address.pin = data['pin']
		address.building = data['building']
		address.room = data['room']
		address.save()
		content = { 'address' : address.address }
		return Response(content,status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	def dispatch(self,*args,**kwargs):
		return super(AddAddress,self).dispatch(*args,**kwargs)

class AddCustomerDetails(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def put(self,request,format=None):
		data = request.body
		data = json.loads(data)
		CustomerDetails(
			customer = request.user,
			phone = data['phone']
		).save()	
		content = {'phone':'added'}
		return Response(content,status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	def dispatch(self,*args,**kwargs):
		return super(AddCustomerDetails,self).dispatch(*args,**kwargs)

















































