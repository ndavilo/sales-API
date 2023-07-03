from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer


class AddOrderItems(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        orderItems = data.get('orderItems', [])

        if not orderItems:
            return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = {
            'user': user.id,
            'paymentMethod': data.get('paymentMethod'),
            'taxPrice': data.get('taxPrice'),
            'shippingPrice': data.get('shippingPrice'),
            'totalPrice': data.get('totalPrice'),
        }
        order_serializer = OrderSerializer(data=order_data)
        order_serializer.is_valid(raise_exception=True)
        order = order_serializer.save()

        for item in orderItems:
            product = Product.objects.get(id=item['product'])
            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=item['qty'],
                price=item['price'],
                image=product.image.url,
            )
            product.countInStock -= order_item.qty
            product.save()

        response_data = OrderSerializer(order).data
        return Response(response_data)


class GetMyOrders(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class GetOrders(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class GetOrderById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            order = Order.objects.get(id=pk)
            if user.is_staff or order.user == user:
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Not Authorized to view this order'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderToPaid(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        order = Order.objects.get(id=pk)
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()
        return Response('Order was paid')


class UpdateOrderToDelivered(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        order = Order.objects.get(id=pk)
        order.isDeliver = True
        order.deliveredAt = datetime.now()
        order.save()
        return Response('Order was Delivered')

