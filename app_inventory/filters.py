from django_filters import CharFilter, FilterSet
from django.db.models import Q

from .models import ProductType, Products


class ProductTypeFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = ProductType
        fields = ['name']


class ProductsFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')
    seller = CharFilter(field_name='seller__first_name', lookup_expr='icontains')
    product_id = CharFilter(field_name='product_type', lookup_expr='exact')
    class Meta:
        model = Products
        fields = ['name', 'seller', 'product_id']