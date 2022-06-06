from django.urls import path, include
from user.views import ProfileListCreateGenericAPIView, ProfileGenericAPIView, LoginAPIView

urlpatterns = [
    path('user/', ProfileListCreateGenericAPIView.as_view()),
    path('user/<pk>/', ProfileGenericAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]
