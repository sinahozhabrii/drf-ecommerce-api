from django.urls import path
from . import views

urlpatterns = [
    
    path('customer/',views.CustomerView.as_view(),name='customer-detail'),
    
    path('products/',views.ProductListCreateView.as_view(),name='product-list'),
    
    path('products/<int:pk>/',views.ProductDetailUpdateDeleteView.as_view(),name='product-detail'),
    
    path('products/categories/',views.CategorysList.as_view(),name='category-list'),
    
    path('product/category/<slug:slug>/',views.CategoryDetail.as_view(),name='category-detail'),
    
    path('cart/create/',views.CartCreateView.as_view(),name='cart-create'),
    
    path('cartitem/create/',views.CartItemCreateView.as_view(),name='cartitem-create'),
    
    path('cart/<uuid:uuid>/item/<int:pk>/delete/',views.CartItemDeleteView.as_view(),name='cartitem-delete'),
    
    path('cart/<uuid:uuid>/item/<int:pk>/update/',views.CartItemUpdateView.as_view(),name='cartitem-update'),
    
    path('cart/<uuid:uuid>/item/<int:pk>/increment/', views.CartItemIncrementView.as_view(), name='cartitem-increment'),
    
    path('cart/<uuid:uuid>/item/<int:pk>/decrement/', views.CartItemDecrementView.as_view(), name='cartitem-decrement'),

    path('cart/<uuid:uuid>/items/',views.CartDetialView.as_view(),name='cart-detial'),
    
    path('order/create/',views.OrderCreateListView.as_view(),name='order-list'),
    
    path('order/<int:pk>/',views.OrderDetailView.as_view(),name='order-detail')
]