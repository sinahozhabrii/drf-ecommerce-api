from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListCreateView.as_view(),name='product-list')
]