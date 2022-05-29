from django.urls import path
from order.views import OrderListView, OrderDetailView, OrderItemDetailView

urlpatterns = [
    path('user/<int:user_pk>/order/', OrderListView.as_view()),
    path('user/<int:user_pk>/order/<int:pk>/', OrderDetailView.as_view()),
    path('user/<int:user_pk>/order/<int:order_pk>/edit/<int:pk>', OrderItemDetailView.as_view()),
]
