from django.contrib import admin

from .models import Products, ProductType, Customer, Order, Debt
from users.models import CustomUser


# Register your models here.
admin.site.register(Products)
admin.site.register(ProductType)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Debt)