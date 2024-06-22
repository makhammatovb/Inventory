from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (ProductTypeViewSet,
                    ProductsViewSet,
                    OrdersViewSet,
                    CustomerViewSet,
                    DebtViewSet,
                    MyOrdersView,
                    # MyDebtsView,
                    my_api_view,
                    home, product_list
)

app_name = 'app_inventory'


router = DefaultRouter()
router.register(r'producttype', ProductTypeViewSet, basename='producttype')
router.register(r'product', ProductsViewSet, basename='product')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'orders', OrdersViewSet, basename='orders')
router.register(r'debt', DebtViewSet, basename='debt')

urlpatterns = router.urls

urlpatterns += [
    path('home/', home, name='home'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
    # path('my-debts/', MyDebtsView.as_view(), name='my_debts'),
    path('my-details/', my_api_view, name='my_details'),
    path('products/', product_list, name='product_list'),
]