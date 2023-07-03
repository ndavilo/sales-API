from rest_framework import serializers
from products.models import Product, Category
from ratings.serializers import RatingSerializer
        
class ProductSerializer(serializers.ModelSerializer):
    product_rating = RatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    category_products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'
        

