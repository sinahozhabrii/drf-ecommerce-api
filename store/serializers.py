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