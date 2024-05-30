from django.db import models
from decimal import Decimal
from datetime import timedelta

from users.models import CustomUser

# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=255)


class Products(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
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
    email = models.EmailField(unique=True, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=30, decimal_places=2, editable=False)
    final_price = models.DecimalField(max_digits=30, decimal_places=2)
    payment = models.DecimalField(max_digits=30, decimal_places=2)
    debt_amount = models.DecimalField(max_digits=30, decimal_places=2, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        self.final_price = self.final_price if self.final_price is not None else Decimal('0.00')
        self.payment = self.payment if self.payment is not None else Decimal('0.00')

        self.total_price = self.product.price * self.quantity
        self.debt_amount = self.final_price - self.payment

        if self.payment == 0:
            self.status = 'canceled'
        elif self.debt_amount > 0:
            self.status = 'pending'
        else:
            self.status = 'completed'

        super(Order, self).save(*args, **kwargs)

        if self.debt_amount > 0:
            Debt.objects.create(
                customer=self.customer,
                product=self.product,
                debt_amount=self.debt_amount,
                due_date=self.date.date() + timedelta(days=60)
            )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Debt(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    debt_amount = models.DecimalField(max_digits=30, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.customer.name} - {self.debt_amount}"

    class Meta:
        db_table = 'debt'
        verbose_name = 'Debt'
        verbose_name_plural = 'Debts'