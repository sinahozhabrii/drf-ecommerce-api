import uuid
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11,blank=True,null=True)
    age = models.DateField(blank=True,null=True)
    
    @property
    def customer_address(self):
        return f"province: {self.address.province}\n-city: {self.address.city}\n-full_address: {self.address.address}"
    
class Address(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,related_name='address')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    descrption = models.TextField(blank=False,null=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL,null=True)
    slug = models.SlugField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class comments(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    body = models.TextField()
    status = models.CharField(choices=COMMENT_STATUS,default=COMMENT_STATUS_WAITING)
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.title

class Discount(models.Model):
    amount = models.FloatField()
    description = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.amount)

class Attribute(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.attribute}-{self.value}'
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product,models.PROTECT,related_name='variants')
    attribute = models.ManyToManyField(AttributeValue)
    inventory = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.ManyToManyField(Discount)
    
    def __str__(self):
        attributes = ", ".join([str(attr) for attr in self.attribute.all()])
        return f"{self.product} - {attributes}"

class Cart(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    
    def __str__(self):
        return str(self.uuid)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.product_variant.price
    
    class Meta:
        unique_together = ('cart', 'product_variant')

class Order(models.Model):
    CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('cancelled', 'لغو شده'),
    ]           
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(blank=True,null=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=CHOICES, default='pending')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        unique_together = ['order','product_variant']