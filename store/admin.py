from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Address)
admin.site.register(models.Attribute)
admin.site.register(models.AttributeValue)
admin.site.register(models.CartItem)
admin.site.register(models.comments)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Discount)
admin.site.register(models.ProductVariant)

class ProductVariantInline(admin.StackedInline):
    model = models.ProductVariant
    extra = 0
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('product',).prefetch_related('discount','attribute__attribute')
    
    
class CartItemInline(admin.StackedInline):
    model = models.CartItem
    extra = 0
    
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    prepopulated_fields = {'slug':['title']}
    list_select_related = ['category']
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related('variants','variants__discount','variants__attribute__attribute')
@admin.register(models.Cart)    
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','description','slug','product_num']
    prepopulated_fields = {'slug':['title']}
    
    def product_num(self,category):
        
        return category.products.all().count()