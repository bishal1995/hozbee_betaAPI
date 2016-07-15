from django.conf.urls import url
import views

urlpatterns = [

	# Add user

    url(r'^addCustomer/$', views.AddUser.as_view() ),
    url(r'^addAddress/$', views.AddAddress.as_view() ),
    url(r'^addCustomerDetails/$', views.AddCustomerDetails.as_view() ),

]

