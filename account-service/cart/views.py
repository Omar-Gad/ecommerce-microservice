from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem

import requests

User = get_user_model()


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        user_pk = self.kwargs['user_pk']
        return get_object_or_404(Cart, user=user_pk)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart = CartDetailView.get_object(self)
        return CartItem.objects.filter(cart=cart.id)


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    
    def get_queryset(self):
        return CartItemDetailView.get_queryset(self)
