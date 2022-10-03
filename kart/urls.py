from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'api/categories', CategoryViewset, basename='category-viewset')
router.register(r'api/products', ProductViewset, basename='product-viewset')

urlpatterns = [
    path('', include(router.urls)),
    path('api/cart/operations/', CartOperationsAPI.as_view(), name="cart-operations"),
    path('api/cart/operations/<id>/', CartOperationsAPI.as_view(), name="cart-operations"),
]