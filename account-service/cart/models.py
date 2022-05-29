from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    quantity = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.IntegerField(default=None)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_item')
