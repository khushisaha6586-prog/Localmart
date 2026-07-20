from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):
    search = request.GET.get("search")
    category = request.GET.get("category")

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category__iexact=category)

    categories = Product.objects.values_list(
        "category", flat=True
    ).distinct()

    return render(request, "products/products.html", {
        "products": products,
        "categories": categories,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, "products/product_detail.html", {
        "product": product
    })