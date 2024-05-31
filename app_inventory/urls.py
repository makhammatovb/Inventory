from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (ProductTypeViewSet,
                    ProductsViewSet,
                    OrdersViewSet,
                    CustomerViewSet,
                    DebtViewSet,
                    MyOrdersView,
                    # MyDebtsView
)

router = DefaultRouter()
router.register(r'producttype', ProductTypeViewSet, basename='producttype')
router.register(r'product', ProductsViewSet, basename='product')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'orders', OrdersViewSet, basename='orders')
router.register(r'debt', DebtViewSet, basename='debt')

urlpatterns = router.urls

urlpatterns += [
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
    # path('my-debts/', MyDebtsView.as_view(), name='my_debts'),
]