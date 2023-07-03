from rest_framework import serializers
from .models import Rating
from products.models import Product

def createProductRating(rating, id):
    product = Product.objects.filter(id=id).first()
    print(rating)
    print(product.rating)
    if product:
        if not product.rating:
            product.rating = int(rating)
            product.numReviews = 1
        else:
            product.rating += int(rating)
            product.numReviews += 1
        product.save()
    
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        
    def validate(self, attrs):
        id = attrs['product'].id
        rating = attrs['rating']

        createProductRating(rating, id)
        return attrs
