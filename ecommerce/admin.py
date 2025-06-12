# shop/admin.py
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model

from .models import Brand, CustomUser, Product, ProductVariant

User = get_user_model()

# ✅ 1. Custom Admin Site
class MyAdminSite(AdminSite):
    site_header = 'Ecommerce Admin Panel'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.count()
        extra_context['total_products'] = Product.objects.count()
        return super().index(request, extra_context)

# ✅ 2. Create admin_site instance
admin_site = MyAdminSite(name='myadmin')

# ✅ 3. Admin registrations use `admin_site`, NOT `admin`
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ('size', 'color', 'stock_count', 'last_updated')
    readonly_fields = ('last_updated',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'is_active')
    inlines = [ProductVariantInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(brand=request.user.brand)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.brand == request.user.brand):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.brand == request.user.brand):
            return True
        return False

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock_count')
    list_filter = ('product__brand',)

# ✅ Register models with the custom admin site
admin_site.register(CustomUser, UserAdmin)
admin_site.register(Brand)
admin_site.register(Product, ProductAdmin)
admin_site.register(ProductVariant, ProductVariantAdmin)
