from rest_framework import viewsets, generics, views
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404

from .models import ProductType, Products, Customer, Order, Debt
from .serializers import ProductTypeSerializer, ProductsSerializer, CustomerSerializer, OrdersSerializer, DebtSerializer
from .permissions import IsAuthorOrReadOnly, IsAdminUser
from .filters import ProductTypeFilter, ProductsFilter


# Create your views here.
class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductTypeFilter


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthorOrReadOnly]


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Debt.objects.all()
        else:
            return Debt.objects.none()


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer__email=user.email)


# class MyDebtsView(views.APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#
#         # Ensure that the user has an associated customer
#         if hasattr(user, 'customer'):
#             customer = user.customer
#             total_debt = Debt.objects.filter(customer=customer).aggregate(total=Sum('debt_amount'))['total'] or 0
#             return Response({'total_debt': total_debt})
#         else:
#             return Response({'error': 'User does not have an associated customer.'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_api_view(request):
    user = request.user
    user_details = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return Response(user_details)


def home(request):
    return render(request, 'inventory/home.html')

def product_list(request):
    products = Products.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Products, pk=product_id)
    return render(request, 'inventory/product_detail.html', {'product': product})