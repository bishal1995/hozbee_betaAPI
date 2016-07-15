from django.shortcuts import render

# Create your views here.
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
from .models import UnitProduct,BundleProduct,FoodTags,TagRelations,LaundryCatalogueItem,FoodCategory
from sales.models import Area
from .serializers import UnitProductSerializer,LaundryCatalogueItemSerializer,FoodCategorySerializer

# get Product details
class ProductDetails(APIView):

    def get(self,request,format=None):
        area = request.META['HTTP_AREA']
        area = int(area)
        try:
            serviceArea = Area.objects.get(area=area)
            products = UnitProduct.objects.filter(service_area=serviceArea)
            serializers = UnitProductSerializer(products,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)

        except Area.DoesNotExist :
            error = {'error':'INVALID_AREA'}
            return Response(error,status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ProductDetails, self).dispatch(*args, **kwargs)

# get Category Details

class CategotyDetails(APIView):

    def get(self,request,format=None) :
        area = request.META['HTTP_AREA']
        area = int(area)
        try:
            serviceArea = Area.objects.get(area=area)
            categories = FoodCategory.objects.filter(service_area=serviceArea)
            serializers = FoodCategorySerializer(categories,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)

        except Area.DoesNotExist :
            error = { 'error':'INVALID_AREA' }
            return Response(error,status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CategotyDetails, self).dispatch(*args, **kwargs)



# get Laundry catalogue
class LaundryDetails(APIView):
    def get(self,request,format=None):
        area = request.META['HTTP_AREA']
        area = int(area)
        try:
            serviceArea = Area.objects.get(area=area)
            laundryItems = LaundryCatalogueItem.objects.filter(service_area=serviceArea)
            serializers = LaundryCatalogueItemSerializer(laundryItems,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)

        except Area.DoesNotExist :
            error = {'error':'INVALID_AREA'}
            return Response(error,status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(LaundryDetails, self).dispatch(*args, **kwargs)






























































