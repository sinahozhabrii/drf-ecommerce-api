from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Address)
admin.site.register(models.Attribute)
admin.site.register(models.AttributeValue)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Category)
admin.site.register(models.comments)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Discount)
admin.site.register(models.ProductVariant)

class ProductVariantInline(admin.StackedInline):
    model = models.ProductVariant
    extra = 0
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    prepopulated_fields = {'slug':['title']}