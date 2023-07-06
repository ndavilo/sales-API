from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductListSet, CategoryListSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('category', CategoryListSet, basename='category')
router.register('staff/products', ProductViewSet, basename='staff_product')
router.register(r'', ProductListSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Add this line
]

