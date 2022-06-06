import requests
from rest_framework import serializers
from cart.models import Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs={'cart': {'read_only': True,}}
        
    def to_representation(self, instance):
        ret =  super().to_representation(instance)
        product_id = ret['product']
        product = requests.get(f'http://host.docker.internal:7000/api/product/{product_id}')
        ret['product'] = product.json()
        return ret
    
    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'
        
        
        