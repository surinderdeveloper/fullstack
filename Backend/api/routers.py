from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'customer', viewsets.CustomerViewSet)
router.register(r'product', viewsets.ProductViewSet)
router.register(r'orders', viewsets.OrdersViewSet)
router.register(r'department', viewsets.DepartmentViewSet)
router.register(r'category', viewsets.CategoryViewSet)