from django.urls import path, include


from rest_framework import routers

from api.views import ProductModelViewSet, CategoryModelViewSet


router = routers.DefaultRouter()

router.register(r'product', ProductModelViewSet, basename='Product')
router.register(r'category', CategoryModelViewSet, basename='Category')

urlpatterns = [
    path('',include(router.urls)),
]

