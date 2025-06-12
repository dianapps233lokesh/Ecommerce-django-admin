from django.contrib import admin
from .models import Brand,Product,Variant,Inventory


admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Inventory)