from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# 1. Custom User
class User(AbstractUser):
    is_brand_admin = models.BooleanField(default=False)
    brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.SET_NULL)

# 2. Brand
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 3. Product
class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

# 4. Inventory
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_count = models.PositiveIntegerField()
    last_updated = models.DateTimeField(default=timezone.now)

# 5. Custom Field (Generic)
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
