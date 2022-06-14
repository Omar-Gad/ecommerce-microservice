import requests
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions, authentication
from order.serializers import OrderSerializer, OrderItemSerializer
from order.models import Order, OrderItem


User = get_user_model()


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        return Order.objects.filter(user=user_pk)


class OrderDetailView(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        order_items = OrderItem.objects.filter(order=instance)
        for item in order_items:
            product = requests.get(
                f'http://host.docker.internal:7000/api/product/{item.product}/').json()
            requests.patch(f'http://host.docker.internal:7000/api/product/{item.product}/',
                           {'quantity': product['quantity']+item.quantity})
        return super().perform_destroy(instance)


class OrderItemDetailView(mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          generics.GenericAPIView):
    serializer_class = OrderItemSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        order_pk = self.kwargs['order_pk']
        return OrderItem.objects.filter(order=order_pk)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def perform_destroy(self, instance):
        product = requests.get(
            f'http://host.docker.internal:7000/api/product/{instance.product}/').json()
        requests.patch(f'http://host.docker.internal:7000/api/product/{instance.product}/',
                       {'quantity': product['quantity']+instance.quantity})
        return super().perform_destroy(instance)
