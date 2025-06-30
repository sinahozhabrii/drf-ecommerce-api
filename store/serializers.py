from pickle import TRUE
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.utils.text import slugify
from . import models


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()
    class Meta:
        model = models.ProductVariant
        fields = ['attributes','inventory','price','discount']
        
    def get_attributes(self, obj):
        return [str(attr) for attr in obj.attribute.all()]
        
class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    class Meta:
        model = models.Product
        fields = ['id','title','descrption','category_title','slug','datetime_created','datetime_modified','variants']
        read_only_fields = ['slug']
        
    def create(self, validated_data):
        title  = validated_data.get('title')
        slug = slugify(title)
        validated_data['slug'] = slug
        return super().create(validated_data)
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['uuid']
        
class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['cart','product_variant','quantity',]
    
    def create(self, validated_data):
        try:
            cart = validated_data['cart']
            product_variant = validated_data['product_variant']
            obj = models.CartItem.objects.get(cart=cart,product_variant=product_variant)
            if obj:
                obj.quantity += validated_data['quantity']
                obj.save()
                return obj
        except:
            
            return super().create(validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    title = serializers.CharField(source='product_variant.product.title')
    cart = serializers.UUIDField(source='cart.uuid')
    
    class Meta:
        model = models.CartItem
        fields = ['cart','title','product_variant','quantity','total_price']
        
class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']
        
class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer()
    product_title = serializers.CharField(source='product_variant.product.title')
    class Meta:
        model = models.OrderItem
        fields = ['product_title','product_variant','quantity','unit_price','items_total_price']
        
class OrderSrializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.user.username')
    items = OrderItemSerializer(many=TRUE)
    class Meta:
        model = models.Order
        fields = ['customer','first_name','last_name','phone_number','province','city','address','email','status','items','datetime_created','datetime_modified','is_paid']
        read_only_fields = ['status','datetime_created','datetime_modified','is_paid','items']
        
class AdminOrderSrializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.user.username')
    items = OrderItemSerializer(many=TRUE)
    class Meta:
        model = models.Order
        fields = ['customer','first_name','last_name','phone_number','province','city','address','email','status','items','datetime_created','datetime_modified','is_paid']      
        
        
        
        
        
class OrderCreateSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = models.Order
        fields = ['uuid','first_name','last_name','phone_number','province','city','address','email']
        read_only_fields = ['status','datetime_created','datetime_modified','is_paid']
    
    def create(self, validated_data,):
        uuid = validated_data.get('uuid')
        cart_obj = get_object_or_404(models.Cart,uuid=uuid)
        user_id = self.context.get('user_id')
        customer = get_object_or_404(models.Customer,user=user_id)
        validated_data.pop('uuid')
        order = models.Order.objects.create(customer=customer,**validated_data)
        cartitems_objs = cart_obj.items.all()
        orderitems_list = []
        for item in cartitems_objs:
            orderitem = models.OrderItem()
            
            orderitem.order = order
            orderitem.product_variant = item.product_variant
            orderitem.quantity = item.quantity
            orderitem.unit_price = item.product_variant.price
            orderitems_list.append(orderitem)
        
        models.OrderItem.objects.bulk_create(orderitems_list)
        cart_obj.delete()
        
        return order
    
    
class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    email = serializers.EmailField(source = 'user.email')
    class Meta:
        model = models.Customer
        fields = ['username','email','phone_number','age']
        
    