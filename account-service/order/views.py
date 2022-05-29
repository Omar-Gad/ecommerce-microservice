from django.contrib.auth import get_user_model
from rest_framework import generics
from order.serializers import OrderSerializer, OrderItemSerializer
from order.models import Order, OrderItem


User = get_user_model()



class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        return Order.objects.filter(user=user_pk)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        return OrderItem.objects.filter(order__user=user_pk)

