from django.contrib import admin
from .models import UnitProduct,BundleProduct,FoodTags,TagRelations,LaundryCatalogueItem,FoodCategory

# Register your models here.

admin.site.register(UnitProduct)
admin.site.register(BundleProduct)
admin.site.register(FoodTags)
admin.site.register(FoodCategory)
admin.site.register(TagRelations)
admin.site.register(LaundryCatalogueItem)
