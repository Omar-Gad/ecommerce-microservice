from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem

from order.models import Order, OrderItem
from order.serializers import OrderSerializer

User = get_user_model()


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        user_pk = self.kwargs['user_pk']
        return get_object_or_404(Cart, user=user_pk)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        cart = CartDetailView.get_object(self)
        return CartItem.objects.filter(cart=cart.id)


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = (TokenAuthentication,)
    
    def get_queryset(self):
        return CartItemDetailView.get_queryset(self)

    def create(self, request, *args, **kwargs):
        cart = request.user.cart
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({'cart':cart})
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
