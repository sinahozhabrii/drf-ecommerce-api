from django.urls import path
from . import views

urlpatterns = [
    
    path('products/',views.ProductListCreateView.as_view(),name='product-list'),
    
    path('products/<int:pk>/',views.ProductDetailUpdateDeleteView.as_view(),name='product-detail'),
    
    path('cart/create/',views.CartCreateView.as_view(),name='cart-create'),
    
    path('cartitem/create/',views.CartItemCreateView.as_view(),name='cartitem-create'),
    
    path('cart/<uuid:uuid>/items/',views.CartDetialView.as_view(),name='cart-detial')
]