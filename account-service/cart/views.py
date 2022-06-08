from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status, views
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
    
    
    def perform_update(self, serializer):
        instance = self.get_object()
        cart = self.request.user.cart
        
        old_quantity = instance.quantity
        
        serializer.save()
        
        cart.quantity -= old_quantity
        cart.total -= old_quantity * serializer.data['product']['price']
        
        cart.quantity += serializer.data['quantity']
        cart.total += serializer.data['quantity']*serializer.data['product']['price']
        
        cart.save()
        

    def perform_destroy(self, instance):
        cart = self.request.user.cart
        serializer = self.get_serializer(instance)
        data = serializer.data

        cart.total -= data['product']['price'] * data['quantity']
        cart.quantity -= instance.quantity
        cart.save()

        instance.delete()
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return CartItemDetailView.get_queryset(self)

    def create(self, request, *args, **kwargs):
        cart = request.user.cart
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data.update({'cart': cart})
        self.perform_create(serializer)

        cart.quantity += serializer.data['quantity']
        cart.total += serializer.data['product']['price'] * serializer.data['quantity']
        cart.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartCheckout(views.APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None, *args, **kwargs):
        cart = request.user.cart
        cart_items = CartItem.objects.filter(cart=cart)
        order = Order.objects.create(total=cart.total, user=cart.user)
        for item in cart_items:
            OrderItem.objects.create(
                quantity=item.quantity, product=item.product, order=order)
        cart.delete()
        Cart.objects.create(user=request.user)
        new_order = OrderSerializer(order).data
        return Response({'New order': new_order})
