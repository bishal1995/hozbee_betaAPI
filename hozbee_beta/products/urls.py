from django.conf.urls import url
import views

urlpatterns = [

	# Get Service Details
    url(r'^productDetails/$', views.ProductDetails.as_view() ),
    url(r'^categoryDetails/$', views.CategotyDetails.as_view() ),
    url(r'^laundryDetails/$', views.LaundryDetails.as_view() ),

]