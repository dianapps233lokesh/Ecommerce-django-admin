# shop/admin.py
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import Brand, CustomUser, Product, ProductVariant

User = get_user_model()


class MyAdminSite(AdminSite):
    site_header = 'Ecommerce Admin Panel'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_users'] = User.objects.count()
        extra_context['total_products'] = Product.objects.count()
        return super().index(request, extra_context)


admin_site = MyAdminSite(name='myadmin')

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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
   
            if 'brand' in form.base_fields:
                form.base_fields['brand'].disabled = True
                form.base_fields['brand'].initial = request.user.brand
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.brand = request.user.brand  
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.brand == request.user.brand)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.brand == request.user.brand)



class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'stock_count')
    list_filter = ('product__brand',)

admin_site.register(Brand)
admin_site.register(Product, ProductAdmin)
admin_site.register(ProductVariant, ProductVariantAdmin)




class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'email', 'brand', 'is_staff', 'is_superuser')


    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Brand Info', {'fields': ('brand',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'brand', 'is_staff', 'is_superuser'),
        }),
    )

admin_site.register(CustomUser, CustomUserAdmin)