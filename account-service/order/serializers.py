import requests
from rest_framework import serializers
from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    
    def to_representation(self, instance):
        ret =  super().to_representation(instance)
        product_id = ret['product']
        product = requests.get(f'http://localhost:7000/api/product/{product_id}')
        ret['product'] = product.json()
        return ret
    
    class Meta:
        model = OrderItem
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'