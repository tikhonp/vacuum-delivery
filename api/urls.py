from django.urls import path
from api import views


urlpatterns = [
    path('order/<int:pk>/', views.SingleOrdersView.as_view()),
    path('orders/active/len/', views.CountActiveOrderSView.as_view()),
]
