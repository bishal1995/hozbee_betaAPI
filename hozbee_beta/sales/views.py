from django.shortcuts import render
# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from products.models import UnitProduct,BundleProduct,FoodTags,TagRelations,LaundryCatalogueItem,FoodCategory
from sales.models import Area,Order,Corder,CorderContent,Cart,CartContent,LaundryCorder,Shipment,Invoice,Transaction,Payment,Tax,Revenue,RevenueGenerated,TaxCollection
from serviceproviders.models import RecievedOrder,SellerDetails
from users.models import CustomerDetails,Address 
from .serializers import CartContentSerializer,CorderSerializer,OrderSerializer,LaundryCorderSerializer
import json,decimal

#Food Orders
# Create Cart and add items to it
class CreateCart(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def put(self,request):
		user = CustomerDetails.objects.get(customer=request.user)
		cartcontent = request.body
		cartcontent = json.loads(cartcontent)
		if ( len(cartcontent['orders']) != 0 ):
			ordered_products = cartcontent['orders']
			cart_validity = True
			products = []
			quantity = []
			half = []
			for order in ordered_products:
				product_id = int(order['product'])
				try:
					product = UnitProduct.objects.get(pk=product_id)
					products.append(product)
					quantity.append(int(order['quantity']))
					half.append(order['half'])
				except UnitProduct.DoesNotExist :
					cart_validity = False
			if ( cart_validity == True ):
				cart = Cart()
				cart.customer = user
				cart.save()
				for i in range(len(products)):
					cart_content = CartContent()
					cart_content.cart = cart
					cart_content.product = products[i]
					cart_content.quantity = quantity[i]
					cart_content.half = half[i]
					cart_content.save()

				cart_details = {'cart_id':cart.cart}
				return Response(cart_details,status=status.HTTP_200_OK)
			else:
				error = {'error':'INVALID_PRODUCTS'}
				return Response(error,status=HTTP_400_BAD_REQUEST)
		else:
			error = {'error':'EMPTY_CART'}
			return Response(error,status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CreateCart, self).dispatch(*args, **kwargs)


# Confirn Order
class ConfirmOrder(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def put(self,request):
		customer = CustomerDetails.objects.get(customer=request.user)
		OrderContent = request.body
		OrderContent = json.loads(OrderContent)
		cart_id = int(OrderContent['cart'])
		address = int(OrderContent['address'])
		payment_mode = OrderContent['payment_mode']
		OrderValidity = True
		try:
			cart = Cart.objects.get(pk=cart_id)
		except Cart.DoesNotExist :
			OrderValidity = False
		try:
			address = Address.objects.get(pk=address)
		except Address.DoesNotExist:
			OrderValidity = False
		paymentModes = ['COD','NET']
		if payment_mode in paymentModes:
			pass
		else:
			OrderValidity = False
		if (OrderValidity == True):
			# Getting Cart Content
			cartcontent = CartContent.objects.filter(cart=cart)
			no_of_orders = len(cartcontent)
			#processing all products in cart
			# Task 1
			# calculating Tax and revenue
			sample_product = cartcontent[0].product
			seller = sample_product.seller
			taxPercent = sample_product.tax_id.tax_percent
			revenuePercent = sample_product.revenue_id.revenue_percentage
			unitTaxes = []
			unitBills = []
			unitPrices = []
			tax = decimal.Decimal(00.00)
			revenue = decimal.Decimal(00.00)
			bill = decimal.Decimal(00.00)
			for i in range(no_of_orders):
				quantity = cartcontent[i].quantity
				if ( cartcontent[i].half == '0' ):
					unitTax = quantity * cartcontent[i].product.price * taxPercent
					unitRevenue = quantity * cartcontent[i].product.price * revenuePercent
					unitbill = quantity * cartcontent[i].product.price + unitTax
					tax = tax + unitTax
					revenue = revenue + unitRevenue
					bill = bill + unitbill
					unitTaxes.append(unitTax)
					unitBills.append(unitbill)
					unitPrices.append(cartcontent[i].product.price)
				else :
					unitTax = quantity * cartcontent[i].product.half_price * taxPercent
					unitRevenue = quantity * cartcontent[i].product.half_price * revenuePercent
					unitbill = quantity * cartcontent[i].product.half_price + unitTax
					tax = tax + unitTax
					revenue = revenue + unitRevenue
					bill = bill + unitbill
					unitTaxes.append(unitTax)
					unitBills.append(unitbill)
					unitPrices.append(cartcontent[i].product.half_price)
			# Saving revenues and taxes
			revenuegen = RevenueGenerated()
			revenuegen.revenue_amount = revenue
			revenuegen.seller = seller
			revenuegen.customer = customer
			revenuegen.save()
			taxcoll = TaxCollection()
			taxcoll.tax_amount = tax
			taxcoll.seller = seller
			taxcoll.customer = customer
			taxcoll.save()
			# Task 2
			# Preparing Corder
			corder = Corder()
			corder.customer = customer
			corder.cart = cart
			corder.address = address
			corder.total_bill = bill
			corder.revenuegenerated = revenuegen
			corder.taxcollection = taxcoll
			corder.save()
			# Task 3
			#Preparing orders for both Seller and Customer and Updating Corder contents
			for j in range(no_of_orders):
				if ( cartcontent[j].half == '0' ) :
					Uorder = Order()
					Uorder.product = cartcontent[j].product
					Uorder.quantity = cartcontent[j].quantity
					Uorder.price = unitPrices[j]
					Uorder.seller = seller
					Uorder.total_amount = unitBills[j]
					Uorder.save()
					CorderContent(
						corder = corder,
						order = Uorder,
						).save()
					RecievedOrder(
						order = Uorder,
						product = cartcontent[j].product,
						half = '0',
						quantity = cartcontent[j].quantity,
						).save()
				else:
					Uorder = Order()
					Uorder.product = cartcontent[j].product
					Uorder.quantity = cartcontent[j].quantity
					Uorder.price = unitPrices[j]
					Uorder.seller = seller
					Uorder.total_amount = unitBills[j]
					Uorder.save()
					CorderContent(
						corder = corder,
						order = Uorder,
						).save()
					RecievedOrder(
						order = Uorder,
						product = cartcontent[j].product,
						half = '1',
						quantity = cartcontent[j].quantity,
						).save()

			# Task 3
			# Generate Invoice 
			invoice = Invoice()
			invoice.delivery_address = address
			invoice.customer = customer
			invoice.customer_name = request.user.first_name + ' ' + request.user.last_name
			invoice.bill = bill
			invoice.save()
			Corder.objects.filter(corder=corder.corder).update(invoice=invoice)
			# Send this invoice to mail and Order confirmation sms to customer
			data = {}
			data['order_status'] = 'confirmed'
			data['Corder_id'] = corder.corder
			return Response(data,status=status.HTTP_200_OK)
		else:
			error = {'error':'INVALID_ORDER_CONFIRMATION'}
			return Response(error,status=status.HTTP_200_OK)
		
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(ConfirmOrder, self).dispatch(*args, **kwargs)


# Transaction Confirmation
# Done by user(online payment) or deliveryboy(COD)
class FoodTransactionConfirmation(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def put(self,request):
		TransactionData = request.body
		TransactionData = json.loads(TransactionData)
		corder = int(TransactionData['corder'])
		amount = decimal.Decimal(TransactionData['amount'])
		mode = TransactionData['mode']
		try:
			CuOrder = Corder.objects.get(corder = corder)
			if ( amount >= CuOrder.total_bill ):
				transaction = Transaction()
				transaction.customer = CuOrder.customer
				transaction.transaction_mode = TransactionData['mode']
				transaction.transaction_amount = amount
				transaction.status = 'DD'
				transaction.save()
				payment = Payment()
				payment.customer = CuOrder.customer
				payment.transaction = transaction
				payment.amount = amount
				payment.payment_mode = TransactionData['mode']
				payment.save()
				updateparameters = {}
				updateparameters['transaction'] = transaction
				updateparameters['payment'] = payment
				Corder.objects.filter(corder=corder).update(**updateparameters)
				data = {'status':'PAYMENT_SUCESSFUL'}
				return Response(data,status=status.HTTP_200_OK)
				# Also might send payment confirmation email or SMS				
			else :
				error = {'error':'AMOUNT_NOT_ACCEPTED'}
				return Response(error,status=status.HTTP_400_BAD_REQUEST)
		except Corder.DoesNotExist :
			error = {'error':'INVALID_CORDER_ID'}
			return Response(error,status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(FoodTransactionConfirmation, self).dispatch(*args, **kwargs)

# Laundry Order
class ConfirmLaundryOrder(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def put(self,request):
		LaundryOrder = request.body
		LaundryOrder = json.loads(LaundryOrder)
		customer = CustomerDetails.objects.get(customer=request.user)
		address_id = int(LaundryOrder['address'])
		try:
			address = Address.objects.get(pk=address_id)
			seller = SellerDetails.objects.get(pk=1) # for codding purpose
			service_requested = LaundryOrder['WD'] + LaundryOrder['WI'] + LaundryOrder['DW']
			LaundryCorder(
				customer = customer,
				address = address,
				service = service_requested,
				seller = seller,
			).save()
			data = {'order':'PLACED_SUCESSFULLY'}
			return Response(data,status=status.HTTP_200_OK)
		except Address.DoesNotExist:
			error = {'error':'INVALID_ADDRESS'}
			return Response(error,status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(ConfirmLaundryOrder,self).dispatch(*args, **kwargs)


# Get All Corders
class FoodOrders(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def get(self,request):
		customer = CustomerDetails.objects.get(customer=request.user)
		Corders = Corder.objects.filter(customer=customer)
		serializers = CorderSerializer(Corders,many=True)
		return Response(serializers.data,status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(FoodOrders,self).dispatch(*args, **kwargs)



# Get all under a Corder
class CorderDetails(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def get(self,request):
		corder_id = int(request.GET['corder'])
		try:
			corder = Corder.objects.get(corder = corder_id)
			orders = CorderContent.objects.filter(corder = corder)
			no_of_orders = len(orders)
			allOrders = []
			for i in range(no_of_orders):
				allOrders.append(orders[i].order)
			serializers = OrderSerializer(allOrders,many=True)
			data = {}
			data['corder_id'] = corder_id
			data['orders'] = serializers.data
			return Response(data,status=status.HTTP_200_OK)
		except Corder.DoesNotExist:
			error = { 'error':'INVALID_CORDER' }
			return Response(error,status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CorderDetails, self).dispatch(*args, **kwargs)

# Get Laundry Order Details
class LaundryOrders(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	throttle_classes = (UserRateThrottle,)

	def get(self,request):
		customer = CustomerDetails.objects.get(customer=request.user)
		allCorders = LaundryCorder.objects.filter(customer=customer)
		serializers = LaundryCorderSerializer(allCorders,many=True)
		return Response(serializers.data,status=status.HTTP_200_OK)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(LaundryOrders, self).dispatch(*args, **kwargs)

