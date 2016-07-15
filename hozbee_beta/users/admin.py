from django.contrib import admin
from .models import Address,CustomerGroup,CustomerDetails
# Register your models here.
admin.site.register(Address)
admin.site.register(CustomerDetails)
admin.site.register(CustomerGroup)

