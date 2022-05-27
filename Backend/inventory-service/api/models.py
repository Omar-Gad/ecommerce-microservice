from django.db import models


def product_image_path(instance, filename):

    return f'photos/product_{instance.product.id}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    description = models.TextField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to=product_image_path)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='image')
    
    def __str__(self):
        return f'{self.product.name} image {self.id}'
