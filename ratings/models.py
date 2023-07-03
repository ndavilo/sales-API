from django.db import models
from allusers.models import User
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

    
class Rating(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True, related_name='product_ratings')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='user_ratings')
    title = models.CharField(max_length=200,null=True,blank=True)
    rating =  models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(10)])
    review = models.TextField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product} - {self.rating}"
    
