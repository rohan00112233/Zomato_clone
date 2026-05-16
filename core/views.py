from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Order, OrderItem
import razorpay
from django.conf import settings


# 🏠 HOME PAGE
def home(request):

    query = request.GET.get('q')

    if query:

        restaurants = Restaurant.objects.filter(
            name__icontains=query
        ) | Restaurant.objects.filter(
            location__icontains=query
        ) | Restaurant.objects.filter(
            cuisine__icontains=query
        )

    else:

        restaurants = Restaurant.objects.all()

    return render(request, 'home.html', {

        'restaurants': restaurants

    })


# 🍽️ RESTAURANT DETAIL PAGE
def restaurant_detail(request, id):

    restaurant = get_object_or_404(Restaurant, id=id)

    return render(request, 'restaurant_detail.html', {

        'restaurant': restaurant

    })


# 🛒 ADD TO CART
@login_required
def add_to_cart(request, id):

    restaurant = Restaurant.objects.get(id=id)

    order, created = Order.objects.get_or_create(

        user=request.user,
        is_completed=False

    )

    item, item_created = OrderItem.objects.get_or_create(

        order=order,
        restaurant=restaurant,

        defaults={

            'price': round(restaurant.rating * 100)

        }

    )

    if not item_created:

        item.quantity += 1

        item.save()

    return redirect('view_cart')


# 🛒 VIEW CART
@login_required
def view_cart(request):

    order = Order.objects.filter(

        user=request.user,
        is_completed=False

    ).first()

    total_price = 0
    total_items = 0

    if order:

        for item in order.items.all():

            item.total_price = item.price * item.quantity

            total_price += item.total_price

            total_items += item.quantity

    final_total = total_price + 40

    return render(request, 'cart.html', {

        'order': order,

        'total_price': total_price,

        'total_items': total_items,

        'final_total': final_total

    })


# ➕ INCREASE QUANTITY
@login_required
def increase_quantity(request, id):

    item = OrderItem.objects.get(id=id)

    item.quantity += 1

    item.save()

    return redirect('view_cart')


# ➖ DECREASE QUANTITY
@login_required
def decrease_quantity(request, id):

    item = OrderItem.objects.get(id=id)

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    else:

        item.delete()

    return redirect('view_cart')


# 💳 PAYMENT PAGE
@login_required
def payment_page(request):

    order = Order.objects.filter(

        user=request.user,
        is_completed=False

    ).first()

    total_price = 0
    total_items = 0

    if order:

        for item in order.items.all():

            item.total_price = item.price * item.quantity

            total_price += item.total_price

            total_items += item.quantity

    final_total = total_price + 40

    client = razorpay.Client(

        auth=(

            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET

        )

    )

    payment = client.order.create({

        'amount': int(final_total * 100),

        'currency': 'INR',

        'payment_capture': '1'

    })

    return render(request, 'payment.html', {

        'order': order,

        'total_price': total_price,

        'total_items': total_items,

        'final_total': final_total,

        'payment': payment,

        'razorpay_key': settings.RAZORPAY_KEY_ID

    })


# 🧾 PLACE ORDER
@login_required
def place_order(request):

    order = Order.objects.filter(

        user=request.user,
        is_completed=False

    ).first()

    if order:

        order.is_completed = True

        order.save()

    return redirect('order_history')


# 📦 ORDER HISTORY
@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    )

    for order in orders:

        order.total_quantity = sum(
            item.quantity for item in order.items.all()
        )

    return render(request, 'order_history.html', {

        'orders': orders

    })