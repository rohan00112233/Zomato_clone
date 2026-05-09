from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, Order, OrderItem


# 🏠 HOME (Search + Listing)
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


# 🍽️ RESTAURANT DETAIL
def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant
    })


# 🛒 ADD TO CART
@login_required
def add_to_cart(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)

    # Get or create order (cart)
    order, created = Order.objects.get_or_create(user=request.user)

    # Get or create item
    item, item_created = OrderItem.objects.get_or_create(
        order=order,
        restaurant=restaurant,
        defaults={'price': restaurant.rating * 100}  # dummy pricing
    )

    # If already exists → increase quantity
    if not item_created:
        item.quantity += 1
        item.save()

    return redirect('view_cart')


# 🛒 VIEW CART
@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user).first()
    return render(request, 'cart.html', {
        'order': order
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

@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user,
        is_completed=True
    )

    return render(request, 'order_history.html', {
        'orders': orders
    })