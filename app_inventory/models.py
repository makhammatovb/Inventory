from django.db import models

from users.models import CustomUser

# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=255)


class Products(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=30, decimal_places=2)
    final_price = models.DecimalField(max_digits=30, decimal_places=2)

    def calculate(self):
        self.total_price = self.product.price * self.quantity
        self.save()

    def __str__(self):
        return self.name
