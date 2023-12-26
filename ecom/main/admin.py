from django.contrib import admin

from .models import ProductDetails,cartProductitems,PurchesDetails

# Register your models here


admin.site.register(ProductDetails)
admin.site.register(cartProductitems)
admin.site.register(PurchesDetails)