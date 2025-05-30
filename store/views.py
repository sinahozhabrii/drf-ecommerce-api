from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializers