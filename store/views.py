import re
from django.shortcuts import get_object_or_404, render
from rest_framework import generics , mixins
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,BasePermission,DjangoModelPermissions
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
    permission_classes = [DjangoModelPermissions]
    
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
        
class CartDetialView(mixins.ListModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer
    lookup_field = 'uuid'
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        models.CartItem.objects.filter(cart__uuid=kwargs['uuid']).delete()
        
        return Response({'detail':'cart is empty'},status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        return super().get_queryset().filter(cart__uuid=uuid).select_related('cart','product_variant__product').prefetch_related('product_variant__attribute__attribute','product_variant__discount')

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = models.CartItem.objects.select_related('cart')
    serializer_class = serializers.CartItemSerializer
    def get_object(self):
        cart_uuid = self.kwargs.get('uuid')
        item = super().get_object()

        if str(item.cart.uuid) != str(cart_uuid):
            raise PermissionDenied("You do not have permission to delete this item.")
    
        return item
    
class CartItemUpdateView(generics.UpdateAPIView):
    queryset = models.CartItem.objects.select_related('cart')
    serializer_class = serializers.CartItemUpdateSerializer
    def get_object(self):
        cart_uuid = self.kwargs.get('uuid')
        item = super().get_object()

        if str(item.cart.uuid) != str(cart_uuid):
            raise PermissionDenied("You do not have permission to delete this item.")
    
        return item
    

    
class OrderCreateListView(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.OrderSrializer
        elif self.request.method == "POST":
            return serializers.OrderCreateSerializer
    def get_queryset(self):
        return super().get_queryset().select_related('customer__user').filter(customer__user=self.request.user)
        
    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['user_id'] = self.request.user.id
        return context
    
    
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = models.Order.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset().select_related('customer__user').filter(customer__user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.user.is_staff and self.request.user.has_perm('store.change_order'):
            return serializers.AdminOrderSrializer
        return serializers.OrderSrializer
    
class CartItemIncrementView(APIView):
            
    def get(self,*args, **kwargs):
        obj = get_object_or_404(models.CartItem,pk=kwargs.get('pk'),cart__uuid=kwargs.get('uuid'))
        obj.quantity +=1
        obj.save()
        return Response({'quantity': obj.quantity}, status=status.HTTP_200_OK)
    
class CartItemDecrementView(APIView):
            
    def get(self,*args, **kwargs):
        obj = get_object_or_404(models.CartItem,pk=kwargs.get('pk'),cart__uuid=kwargs.get('uuid'))
        if obj.quantity>1:
            obj.quantity -=1
            obj.save()
        else:
            obj.delete()
        return Response({'quantity': obj.quantity}, status=status.HTTP_200_OK)