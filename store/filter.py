# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(method='filter_price_min')
    price_max = django_filters.NumberFilter(method='filter_price_max')
    category = django_filters.CharFilter(method='filter_category')

    class Meta:
        model = Product
        fields = []

    def filter_price_min(self, queryset, name, value):
        print(name)
        return queryset.filter(variants__price__gte=value)

    def filter_price_max(self, queryset, name, value):
        return queryset.filter(variants__price__lte=value)
    
    def filter_category(self,queryset,name,value):
        return queryset.filter(category__title=value)
