from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductListSet, CategoryListSet, ProductListByCategoryView

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('category', CategoryListSet, basename='category')
router.register('staff/products', ProductViewSet, basename='staff_product')
router.register(r'', ProductListSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # Add this line
    path('products/productlist/category=<int:id>/', ProductListByCategoryView.as_view(), name='product-list-by-category'),
]

