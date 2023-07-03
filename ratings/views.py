from rest_framework.permissions import AllowAny
from rest_framework import filters
from rest_framework import generics
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.permissions import IsAdminUser

class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product']

    def get_queryset(self):
        return Rating.objects.all()

class RatingDeleteView(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser]


