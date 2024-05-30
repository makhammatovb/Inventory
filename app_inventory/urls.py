from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductTypeViewSet, ProductsViewSet, OrdersViewSet, CustomerViewSet, DebtViewSet, MyOrdersView

router = DefaultRouter()
router.register(r'producttype', ProductTypeViewSet, basename='producttype')
router.register(r'product', ProductsViewSet, basename='product')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'orders', OrdersViewSet, basename='orders')
router.register(r'debt', DebtViewSet, basename='debt')
# router.register(r'my-orders', MyOrdersView, basename='my-orders')

urlpatterns = router.urls

urlpatterns += [
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
]