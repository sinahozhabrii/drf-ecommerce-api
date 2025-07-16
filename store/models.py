import uuid
from django.db import models
from django.contrib.auth import get_user_model
from helpers import cloudinary_init
from cloudinary.models import CloudinaryField

cloudinary_init()


def get_public_id_prefix(obj):
    if hasattr(obj,'title'):
        if hasattr(obj,'category'):
            return f'{obj.slug}-{obj.category}'
        else:
            return f'{obj.slug}'
    elif hasattr(obj,'proudct'):
        return f'{obj.product.slug}-{obj.product.category}-{obj.attribute}'
    
    elif hasattr(obj,'user'):
        return f'{obj.user.username}-profile_upload'
    obj_class = obj.__class__
    obj_class_name = obj_class.__name__
    
    return f'{obj_class_name}-upload'

def get_display_name(obj):
    if hasattr(obj,'title'):
        if hasattr(obj,'category'):
            return f'{obj.slug}-{obj.category}'
        else:
            return f'{obj.slug}'
    elif hasattr(obj,'proudct'):
        return f'{obj.product.slug}-{obj.product.category}-{obj.attribute}'
    
    elif hasattr(obj,'user'):
        return f'{obj.user.username}-profile_upload'
    
    obj_class = obj.__class__
    obj_class_name = obj_class.__name__
    
    return f'{obj_class_name}-upload'
# Create your models here.
class Customer(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    profile_image = CloudinaryField(
                            'image',blank=True,null=True,
                            
                            public_id_prefix=get_public_id_prefix,
                            
                            display_name = get_display_name,
                            
                            tags = ['product']
                            )
    phone_number = models.CharField(max_length=11,blank=True,null=True)
    age = models.DateField(blank=True,null=True)
    
    @property
    def customer_address(self):
        return f"province: {self.address.province}\n-city: {self.address.city}\n-full_address: {self.address.address}"
    
    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,related_name='address')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    
        
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False,null=True)
    image = CloudinaryField(
                            'image',blank=True,null=True,
                            
                            public_id_prefix=get_public_id_prefix,
                            
                            display_name = get_display_name,
                            
                            tags = ['product']
                            )
    category = models.ForeignKey("Category", on_delete=models.SET_NULL,null=True,related_name='products')
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
    image = CloudinaryField(
                            'image',blank=True,null=True,
                            
                            public_id_prefix=get_public_id_prefix,
                            
                            display_name = get_display_name,
                            
                            tags = ['product']
                            )
    slug = models.SlugField()
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
    image = CloudinaryField(
                            'image',blank=True,null=True,
                            
                            public_id_prefix=get_public_id_prefix,
                            
                            display_name = get_display_name,
                            
                            tags = ['product']
                            )
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
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.product_variant.price

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
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)
    
    @property
    def items_total_price(self):
        return self.quantity * self.unit_price
    
    class Meta:
        unique_together = ['order','product_variant']
        
