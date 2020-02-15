from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract=True

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user  = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)

        user.is_admin = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):

    email               = models.EmailField(
    						verbose_name='email address',
    						max_length=255,
    						unique=True,
    					)
    created_date        = models.DateTimeField(auto_now_add=True, editable=False)
    is_active 			= models.BooleanField(default=True)
    is_admin    		= models.BooleanField(default=False)
    first_name	        = models.CharField(max_length=255, blank=True, null=True)
    last_name	        = models.CharField(max_length=255, blank=True, null=True) 
    credit_card 		= models.CharField(max_length=255, blank=True, null=True)
    address_1   		= models.CharField(max_length=255, blank=True, null=True)
    address_2			= models.CharField(max_length=255, blank=True, null=True)
    city	    		= models.CharField(max_length=255, blank=True, null=True)
    region	    		= models.CharField(max_length=255, blank=True, null=True)
    postal_code	       	= models.CharField(max_length=255, blank=True, null=True)
    country	           	= models.CharField(max_length=255, blank=True, null=True)
    shipping_region_id 	= models.IntegerField(default=1)
    day_phone	       	= models.CharField(max_length=255, blank=True, null=True)
    eve_phone	       	= models.CharField(max_length=255, blank=True, null=True)
    mob_phone	       	= models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):

        return self.filename + ' ' + self.last_name

    def get_short_name(self):

        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Department(BaseModel):

	name        = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name

class Category(models.Model):

	department  = models.ForeignKey(Department, on_delete=models.CASCADE,)
	name        = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'

def product_directory_path(instance, filename):
    return 'projects/{0}_{1}'.format(instance.created_date, filename)

class Product(BaseModel):

	name        = models.CharField(max_length=100)
	description = models.TextField()
	price       = models.DecimalField(max_digits=10, decimal_places=2)
	discounted_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
	image      = models.ImageField(upload_to=product_directory_path)
	image_2    = models.ImageField(upload_to=product_directory_path)
	thumbnail  = models.ImageField(upload_to=product_directory_path)
	display    = models.SmallIntegerField(default=0)

	def __str__(self):
		return self.name

class ProductCategory(models.Model):

	product = models.ForeignKey(Product)
	category = models.ForeignKey(Category)

	def __str__(self):
		return self.category.name

class Attribute(models.Model):

	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Product Attribute'
		verbose_name_plural = 'Product Attributes'


class AttributeValue(models.Model):

	attribute = models.ForeignKey(Attribute)
	value     = models.CharField(max_length=100)

	def __str__(self):
		return self.value

from django.utils.html import format_html
class ProductAttribute(models.Model):
    
    product = models.ForeignKey(Product)
    attribute_value  = models.ForeignKey(AttributeValue)

    def __str__(self):
        return self.attribute_value.value

class ShoppingCart(models.Model):

    cart_id    = models.CharField(max_length=32)
    product    = models.ForeignKey(Product)
    attributes = models.CharField(max_length=100)
    quantity   = models.IntegerField()
    buy_now    = models.BooleanField(default=True)
    added_on   = models.DateTimeField(auto_now=True)

class ShippingRegion(models.Model):

	shipping_region = models.CharField(max_length=100)

	def __str__(self):
		return self.shipping_region

class Shipping(BaseModel):

	shipping_type   = models.CharField(max_length=100)
	shipping_cost   = models.DecimalField(max_digits=10, decimal_places=2)
	shipping_region = models.ForeignKey(ShippingRegion)

	def __str__(self):
		return self.shipping_type

class Tax(BaseModel):

	tax_type = models.CharField(max_length=100)
	tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.tax_type

class Orders(BaseModel):

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipped_on   = models.DateTimeField()
    status       = models.CharField(max_length=255)
    comments     = models.CharField(max_length=255)
    customer     = models.ForeignKey(Customer)
    auth_code    = models.CharField(max_length=50)
    reference    = models.CharField(max_length=50)
    shipping_id  = models.ForeignKey(Shipping)
    tax_id       = models.ForeignKey(Tax)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderDetail(BaseModel):

    order        = models.ForeignKey(Orders)
    product      = models.ForeignKey(Product)
    attributes   = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    quantity     = models.IntegerField()
    unit_cost    = models.DecimalField(max_digits=10, decimal_places=2)

class Audit(BaseModel):

    order      = models.ForeignKey(Orders)
    message    = models.TextField()
    code       = models.IntegerField()

class Review(BaseModel):

    customer   = models.ForeignKey(Customer)
    product    = models.ForeignKey(Product)
    review     = models.TextField()
    rating     = models.SmallIntegerField()


