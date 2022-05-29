from django.shortcuts import get_object_or_404
from rest_framework import serializers
from api.models import Product, Category, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    image = ProductImageSerializer(many=True, read_only=True)
    image_upload = serializers.ImageField(write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image_upload')
        
        category_name = validated_data.pop('category')
        category = get_object_or_404(Category, name=category_name)
        serializers.ValidationError('category not found')
        validated_data['category'] = category
        
        product = Product(**validated_data)
        product.save()
        
        ProductImage(image=image, product=product).save()

        return product

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category')
        category = get_object_or_404(Category, name=category_name)
        validated_data['category'] = category
        
        instance = super().update(instance, validated_data)
        return instance
