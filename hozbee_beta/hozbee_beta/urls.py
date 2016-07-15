"""hozbee_beta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', views.obtain_auth_token),

    url(r'^users/', include('users.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^sales/', include('sales.urls')),
#    url(r'^cdn/', include('cdn.urls')),

#    url(r'^reviewandrating/', include('reviewandrating.urls')),
#    url(r'^serviceproviders/', include('serviceproviders.urls')),
#    url(r'^staff/', include('staff.urls')),
]