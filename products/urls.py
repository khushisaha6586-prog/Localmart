from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),

    # Product Detail Page
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]