from django.urls import path
from .views import RatingCreateView, RatingDeleteView, RatingListView

urlpatterns = [
    path('', RatingCreateView.as_view(), name='rating_create'),
    path('list/', RatingListView.as_view(), name='rating_list'),
    path('<int:pk>/delete/', RatingDeleteView.as_view(), name='rating_delete'),
]
