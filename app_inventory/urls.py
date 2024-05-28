from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductTypeViewSet, ProductsViewSet, OrdersViewSet, CustomerViewSet

router = DefaultRouter()
router.register(r'producttype', ProductTypeViewSet)
router.register(r'product', ProductsViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'orders', OrdersViewSet)

urlpatterns = router.urls
