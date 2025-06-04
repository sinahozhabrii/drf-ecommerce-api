from django.shortcuts import render
from rest_framework import generics , mixins
from . import models
from . import serializers
# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('variants__attribute__attribute','variants__discount').select_related('category')

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related('variants__attribute__attribute','variants__discount').select_related('category')

class CartCreateView(generics.CreateAPIView):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    
class CartItemCreateView(generics.CreateAPIView):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemCreateSerializer
    
    def get_queryset(self):
        return models.CartItem.objects.all().select_related('product_variant__product',).prefetch_related('product_variant__attribute__attribute','product_variant__discount')
        
class CartDetialView(mixins.ListModelMixin,generics.GenericAPIView):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    lookup_field = 'uuid'
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        return super().get_queryset().filter(cart__uuid=uuid).select_related('cart','product_variant__product').prefetch_related('product_variant__attribute__attribute','product_variant__discount')

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    
class OrderCreateListView(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.OrderSrializer
        elif self.request.method == "POST":
            return serializers.OrderCreateSerializer
    def get_queryset(self):
        return super().get_queryset().select_related('customer__user')
        
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context