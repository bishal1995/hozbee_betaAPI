from django.conf.urls import url
from django.views.decorators.cache import cache_page
import views

urlpatterns = [

	# Get Service Details
    url(r'^productDetails/$', cache_page(86400)(views.ProductDetails.as_view()) ),
    url(r'^categoryDetails/$', cache_page(86400)(views.CategotyDetails.as_view()) ),
    url(r'^laundryDetails/$', cache_page(86400)(views.LaundryDetails.as_view()) ),

]