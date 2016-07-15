from django.conf.urls import url
import views

urlpatterns = [
	
    url(r'^createCart/$', views.CreateCart.as_view() ),
    url(r'^confirmOrder/$', views.ConfirmOrder.as_view() ),
    url(r'^confirmFtransaction/$', views.FoodTransactionConfirmation.as_view() ),
    url(r'^confirmLaundryorder/$', views.ConfirmLaundryOrder.as_view() ),
    url(r'^allCorder/$', views.FoodOrders.as_view() ),
    url(r'^allOrder/$', views.CorderDetails.as_view() ),
    url(r'^allLorder/$', views.LaundryOrders.as_view() ),


]

