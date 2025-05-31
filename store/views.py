from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    def get_queryset(self):
        return super().get_queryset().prefetch_related('variants__attribute','variants__attribute__attribute','variants__discount').select_related('category')

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    def get_queryset(self):
        return super().get_queryset().prefetch_related('variants__attribute','variants__attribute__attribute','variants__discount').select_related('category')

class CartCreateView(generics.CreateAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    
class CartCreateView(generics.CreateAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    