from rest_framework import serializers

from .models import ProductType, Products, Customer, Order, Debt
from users.models import CustomUser


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name']


class NameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ['name']


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ['name']


class ProductsSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    product_type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())

    class Meta:
        model = Products
        fields = ['product_type', 'name', 'price', 'quantity', 'seller']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['seller'] = request.user
        return Products.objects.create(**validated_data)


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['name']


class OrdersSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=30, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'date', 'product', 'quantity', 'total_price', 'final_price', 'name', 'customer', 'payment', 'debt_amount']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product and quantity:
            if product.quantity < quantity:
                raise serializers.ValidationError({
                    'quantity': 'The quantity requested exceeds the available inventory.'
                })

        return data

    def create(self, validated_data):
        request = self.context.get('request')

        product = validated_data['product']
        quantity = validated_data['quantity']
        total_price = product.price * quantity

        validated_data['total_price'] = total_price

        product.quantity -= quantity
        product.save()

        order = Order.objects.create(**validated_data)
        return order


class DebtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Debt
        fields = ['id', 'date', 'product', 'customer', 'due_date']