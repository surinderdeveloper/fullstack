from django.contrib import admin
from django.contrib.auth.models import Group
from jet.admin import CompactInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer, Department, Category, Product, ProductCategory,\
   Attribute, AttributeValue, ProductAttribute, ShoppingCart, ShippingRegion,\
   Shipping, Tax, Orders, OrderDetail, Audit, Review


@admin.register(Customer)
class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'first_name', 'is_active')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','credit_card','address_1','address_2'
        	,'city', 'region', 'postal_code', 'country', 'shipping_region_id', 
        	'day_phone','eve_phone','mob_phone')}),
        ('Permissions', {'fields': ('is_admin','is_active')}),
        (('Important dates'), {'fields': ('last_login','created_date')}),
    )
    readonly_fields = ('created_date',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2','credit_card','address_1','address_2'
        	,'city', 'region', 'postal_code', 'country', 'shipping_region_id', 
        	'day_phone','eve_phone','mob_phone')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'department',)
    list_filter = ('department',)
    search_fields = ('name',)

class AttributeValueInline(CompactInline):
    model = AttributeValue
    extra = 0
    show_change_link = True

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = (AttributeValueInline,)

class ProductAttributeInline(CompactInline):
    
    model  = ProductAttribute
    extra  = 0
    show_change_link = True

class ProductCategoryAdmin(CompactInline):

    model = ProductCategory
    extra = 0
    show_change_link = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = (ProductCategoryAdmin, ProductAttributeInline)
    list_display = ('name', 'description','price', 'discounted_price')
    search_fields = ('name',)

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('product', 'attributes', 'quantity')
    list_filter = ('attributes','product')

@admin.register(ShippingRegion)
class ShippingRegionAdmin(admin.ModelAdmin):

    list_display = ('shipping_region', )
    search_fields = ('shipping_region',)

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):

    list_display = ('shipping_type', 'shipping_cost', )
    list_filter = ('shipping_region',)
    search_fields = ('shipping_type','shipping_cost')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):

    list_display = ('tax_type', 'tax_percentage')
    search_fields = ('tax_type','tax_percentage')

# @admin.register(OrderDetail)
class OrderDetailAdmin(admin.StackedInline):

    model = OrderDetail
    extra = 0
    show_change_link = True

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):

    inlines = (OrderDetailAdmin,)
    list_display = ('total_amount', 'shipped_on',)

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):

    list_display = ('order', 'message', 'code')
    list_filter = ('order',)
    search_fields = ('message',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ('review', 'rating', 'customer', 'product') 
    list_filter = ('customer','product')
    search_fields = ('review',)  

# unregister the Group model from admin.
admin.site.unregister(Group)

