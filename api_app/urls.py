from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.product_list, name="api_products"),
    path("products/<int:pk>/", views.product_detail, name="api_product_detail"),
    path("cart/", views.cart_list, name="api_cart"),
    path("orders/", views.order_list, name="api_orders"),
    path("profile/<int:pk>/", views.profile, name="api_profile"),
]