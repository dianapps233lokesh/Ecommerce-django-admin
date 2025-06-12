# from django.contrib.admin import AdminSite
# from django.template.response import TemplateResponse
# from django.contrib.auth import get_user_model
# from .models import Product, ProductVariant
# from .models import CustomUser, Brand, Product, ProductVariant
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# User = get_user_model()

# class MyAdminSite(AdminSite):
#     site_header = 'Ecommerce Admin Panel'

#     def index(self, request, extra_context=None):
#         extra_context = extra_context or {}
#         extra_context['total_users'] = User.objects.count()
#         extra_context['total_products'] = Product.objects.count()
#         return super().index(request, extra_context)

# admin_site = MyAdminSite(name='myadmin')
# admin_site.register(CustomUser, UserAdmin)
# admin_site.register(Brand)
# admin_site.register(Product, ProductAdmin)
# admin_site.register(ProductVariant, ProductVariantAdmin)