from rest_framework import serializers
from . import models

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    
    class Meta:
        model = models.ProductCategory
        fields = '__all__'

    def get_category(self, obj):
    	return obj.category.name

class ProductAttributeSerializer(serializers.ModelSerializer):
    
    attribute_value = serializers.SerializerMethodField()
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = models.ProductAttribute
        fields = '__all__'

    def get_attribute_value(self, obj):
    	return obj.attribute_value.value

    def get_attribute(self, obj):
    	return obj.attribute_value.attribute.name

class ProductSerializer(serializers.ModelSerializer):
    
    product_category = serializers.SerializerMethodField()
    product_attribute = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_product_category(self, obj):
        return [ProductCategorySerializer(s).data for s in obj.productcategory_set.all()]

    def get_product_attribute(self, obj):
        return [ProductAttributeSerializer(s).data for s in obj.productattribute_set.all()]

class OrderDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.OrderDetail
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    
    detail = OrderDetailSerializer()

    class Meta:
        model = models.Orders
        fields = '__all__'
