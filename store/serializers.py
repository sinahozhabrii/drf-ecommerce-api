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