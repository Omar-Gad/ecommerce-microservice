from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    quantity = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def update_cart_data(self,oldq=0,oldt=0,newq=0,newt=0,method=None):
        if method == 'create':
            self.quantity += newq
            self.total += newt
        elif method == 'update':
            self.quantity -= oldq
            self.total -= oldt
            self.quantity += newq
            self.total += newt
        elif method == 'delete':
            self.quantity -= oldq
            self.total -= oldt
        
        self.save()
    
    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(models.Model):
    quantity = models.IntegerField(default=0)
    product = models.IntegerField(default=None)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_item')
    
    def __str__(self):
        return f"cart item {self.id}"
