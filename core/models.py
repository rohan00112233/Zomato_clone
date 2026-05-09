from django.db import models
from django.conf import settings



# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100) 
    rating = models.FloatField()   
    image = models.URLField()

    def __str__(self):
        return self.name
    

class Order(models.Model):   # ✅ correct name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # ✅ fixed
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        return self.restaurant.name