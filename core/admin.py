from django.contrib import admin
from .models import Restaurant, Order, OrderItem

admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(OrderItem)
# Register your models here.
