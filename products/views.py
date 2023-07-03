from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.db.models import Q
from rest_framework import filters
from rest_framework.response import Response

class ProductPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ProductPagination


class ProductListSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name']
    ordering_fields = ['name', 'price', 'discount', 'rating']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filters
        name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')
        amount = self.request.query_params.get('amount')
        discount = self.request.query_params.get('discount')
        rating = self.request.query_params.get('rating')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category:
            queryset = queryset.filter(category__name=category)
        if amount:
            queryset = queryset.filter(price=amount)
        if discount:
            queryset = queryset.filter(discount=discount)
        if rating:
            queryset = queryset.filter(rating=rating)

        return queryset