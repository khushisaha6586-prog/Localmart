from mongodb import orders_collection
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from threading import Thread
import time

from cart.models import Cart
from .models import Order
from .models import Order , Notification 


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, "orders/orders.html", {
        "orders": orders
    })


def send_notification(product_name):
    time.sleep(2)
    print(f"Notification: Order for '{product_name}' placed successfully!")


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart_list")

    for item in cart_items:

        product = item.product

        if product.stock == 0:
            return render(request, "orders/out_of_stock.html", {
                "product": product
            })

        if product.stock < item.quantity:
            return render(request, "orders/out_of_stock.html", {
                "product": product
            })

        Order.objects.create(
            user=request.user,
            product=product,
            quantity=item.quantity
        )
        Notification.objects.create(
            user=request.user,
            message=f"Your order for '{product.name}' has been placed successfully."
            )
        orders_collection.insert_one({
            "username": request.user.username,
            "product": product.name,
            "quantity": item.quantity,
            "price": float(product.price),
            "status": "Pending"
            })

        Thread(
            target=send_notification,
            args=(product.name,)
        ).start()

        product.stock -= item.quantity
        product.save()

    cart_items.delete()

    return redirect("order_list")
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/notifications.html",
        {"notifications": notifications}
    )