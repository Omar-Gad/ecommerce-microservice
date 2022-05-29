from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItem(models.Model):
    quantity = models.IntegerField()
    product = models.IntegerField()
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_item')