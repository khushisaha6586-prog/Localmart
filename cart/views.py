from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart
from products.models import Product
from mongodb import cart_collection


@login_required
def cart_list(request):
    carts = Cart.objects.filter(user=request.user)

    # Calculate Grand Total
    grand_total = 0
    for cart in carts:
        grand_total += cart.product.price * cart.quantity

    return render(request, "cart/cart.html", {
        "carts": carts,
        "grand_total": grand_total,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Save/Update Cart in MongoDB
    cart_collection.update_one(
        {
            "username": request.user.username,
            "product": product.name
        },
        {
            "$set": {
                "quantity": cart_item.quantity,
                "price": float(product.price)
            }
        },
        upsert=True
    )

    return redirect("cart_list")


@login_required
def increase_quantity(request, cart_id):
    cart = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart.quantity += 1
    cart.save()

    # Update MongoDB
    cart_collection.update_one(
        {
            "username": request.user.username,
            "product": cart.product.name
        },
        {
            "$set": {
                "quantity": cart.quantity,
                "price": float(cart.product.price)
            }
        },
        upsert=True
    )

    return redirect("cart_list")


@login_required
def decrease_quantity(request, cart_id):
    cart = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()

        # Update MongoDB
        cart_collection.update_one(
            {
                "username": request.user.username,
                "product": cart.product.name
            },
            {
                "$set": {
                    "quantity": cart.quantity,
                    "price": float(cart.product.price)
                }
            },
            upsert=True
        )
    else:
        # Remove from MongoDB
        cart_collection.delete_one({
            "username": request.user.username,
            "product": cart.product.name
        })
        cart.delete()

    return redirect("cart_list")


@login_required
def remove_from_cart(request, cart_id):
    cart = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    # Remove from MongoDB
    cart_collection.delete_one({
        "username": request.user.username,
        "product": cart.product.name
    })

    cart.delete()

    return redirect("cart_list")