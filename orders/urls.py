from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    AddOrderItems,
    GetMyOrders,
    GetOrders,
    GetOrderById,
    UpdateOrderToPaid,
    UpdateOrderToDelivered,
)

urlpatterns = [
    path('add/', AddOrderItems.as_view(), name='add-order-items'),
    path('my/', GetMyOrders.as_view(), name='get-my-orders'),
    path('all/', GetOrders.as_view(), name='get-all-orders'),
    path('<int:pk>/', GetOrderById.as_view(), name='get-order-by-id'),
    path('<int:pk>/paid/', UpdateOrderToPaid.as_view(), name='update-order-to-paid'),
    path('<int:pk>/delivered/', UpdateOrderToDelivered.as_view(), name='update-order-to-delivered'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
