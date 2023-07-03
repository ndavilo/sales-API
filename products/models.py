from django.db import models
from django.core.exceptions import ValidationError
from allusers.models import User
import random
import string
from django.core.files.storage import default_storage


def generate_random_id():
    while True:
        random_id = ''.join(random.choices(string.digits, k=16))
        if not Product.objects.filter(id=random_id).exists():
            return random_id
        
def validate_image_file(image):
    max_size = 10 * 1024 * 1024  # Example: limit to 10 MB
   
    if image.size > max_size:
        raise ValidationError('File size exceeds the limit.')



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(primary_key=True, default=generate_random_id, max_length=16, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        null=True,
        blank=True,
        default="/products/placeholder.png",
        upload_to="products/",
        validators=[validate_image_file]
    )
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.price}"

    def delete(self, *args, **kwargs):
        # Delete the product image from storage
        if self.image:
            default_storage.delete(self.image.name)
        super().delete(*args, **kwargs)