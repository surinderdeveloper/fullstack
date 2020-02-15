from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CustomerSerializer, ProductSerializer, OrdersSerializer,\
                                            DepartmentSerializer, CategorySerializer
from .models import Customer, Product, Orders, Department, Category


class CustomerViewSet(viewsets.ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = {'department' :['in'], }

class ProductViewSet(viewsets.ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = {'name' :['icontains'], 'price' :['gte', 'lte'], 
            'productcategory__category__name' :['in'],'productattribute__attribute_value__value' :['in'],}

class OrdersViewSet(viewsets.ModelViewSet):
    
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
