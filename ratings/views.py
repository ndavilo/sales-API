from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework import generics
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.permissions import IsAdminUser

class ProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_id = request.query_params.get('product')
        if product_id:
            return queryset.filter(product_id=product_id)
        return queryset
    
class RatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]
    filter_backends = [ProductFilter, filters.OrderingFilter]
    filterset_fields = ['product_id']

    def get_queryset(self):
        return Rating.objects.all()

class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingDeleteView(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser]


