from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_list, name="cart_list"),

    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    path("increase/<int:cart_id>/", views.increase_quantity, name="increase_quantity"),

    path("decrease/<int:cart_id>/", views.decrease_quantity, name="decrease_quantity"),

    path("remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
]