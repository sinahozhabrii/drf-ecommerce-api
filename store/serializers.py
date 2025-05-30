from rest_framework import serializers
from django.utils.text import slugify
from . import models

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['title','descrption','category','slug','datetime_created','datetime_modified','variants']
        read_only_fields = ['slug']
        
    def create(self, validated_data):
        title  = validated_data.get('title')
        slug = slugify(title)
        validated_data['slug'] = slug
        return super().create(validated_data)
        