import requests
from rest_framework import serializers
from cart.models import Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

def get_product(id):
    return requests.get(f'http://host.docker.internal:7000/api/product/{id}')


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs={'cart': {'read_only': True,}}
        
    def to_representation(self, instance):
        ret =  super().to_representation(instance)
        product_id = ret['product']
        product = get_product(product_id)
        ret['product'] = product.json()
        return ret
    
    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        method = self.context['request'].method

        if method in ['PUT', 'PATCH']:
            kwargs = extra_kwargs.get('product', {})
            kwargs['read_only'] = True
            extra_kwargs['product'] = kwargs

        return extra_kwargs
    
    def validate(self, data):
        method = self.context['request'].method
        
        if  method in ['PUT', 'PATCH']:
            instance = self.context['instance']
            product_id = instance.product
            product = get_product(product_id).json()
            
        elif method == 'POST':
            product_id = data['product']
            product = get_product(product_id).json()
        
        if data['quantity'] > product['quantity']:
            raise serializers.ValidationError("Not enough in stock")
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be more than 0")
        
        return data
    

class CartSerializer(serializers.ModelSerializer):
    cart_item = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'
        