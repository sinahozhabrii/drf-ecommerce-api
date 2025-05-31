from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.ProductListCreateView.as_view(),name='product-list'),
    path('products/<int:pk>/',views.ProductDetailUpdateDeleteView.as_view(),name='product-detail'),
    path('cart/create/',views.CartCreateView.as_view(),name='cart-create')
]