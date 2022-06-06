from django.urls import path, include
from cart.views import CartDetailView, CartItemDetailView, CartItemCreateView, CartCheckout

urlpatterns = [
    path('user/<int:user_pk>/cart/',CartDetailView.as_view()),
    path('user/<int:user_pk>/cart/<int:pk>/',CartItemDetailView.as_view()),
    path('user/<int:user_pk>/cart/add/',CartItemCreateView.as_view()),
    path('user/<int:user_pk>/cart/checkout/',CartCheckout.as_view()),
]