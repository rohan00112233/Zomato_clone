from django.urls import path
from .views import home
from . import views
urlpatterns = [
    path('', home, name='home'),
    path('restaurant/<int:id>/', views.restaurant_detail, name='restaurant_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('payment/', views.payment_page, name='payment_page'),   
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path(
    'increase-quantity/<int:id>/',
    views.increase_quantity,
    name='increase_quantity'
),

path(
    'decrease-quantity/<int:id>/',
    views.decrease_quantity,
    name='decrease_quantity'
),

path(
    'api/restaurants/',
    views.restaurant_api,
    name='restaurant_api'
),

path(
    'api/restaurants/<int:id>/',
    views.restaurant_detail_api,
    name='restaurant_detail_api'
),

path(
    'api/add-restaurant/',
    views.add_restaurant_api,
    name='add_restaurant_api'
),

path(
    'api/update-restaurant/<int:id>/',
    views.update_restaurant_api,
    name='update_restaurant_api'
),
path(
    'api/add-restaurant/',
    views.add_restaurant_api,
    name='add_restaurant_api'
),

path(
    'api/update-restaurant/<int:id>/',
    views.update_restaurant_api,
    name='update_restaurant_api'
),

path(
    'api/delete-restaurant/<int:id>/',
    views.delete_restaurant_api,
    name='delete_restaurant_api'
)
]