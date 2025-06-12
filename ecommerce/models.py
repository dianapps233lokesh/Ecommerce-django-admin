from django.contrib.auth.models import User
from django.db import models


class Brand(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Variant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variant_name=models.CharField(max_length=200)


    def __str__(self):
        return f"{self.product}-{self.variant}"

class Inventory(models.Model):
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE)
    stock_count=models.IntegerField()
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return  {self.variant}-{self.stock_count}

