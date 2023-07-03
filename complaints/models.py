from django.db import models
from allusers.models import User

# Create your models here.
class Complaint(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_complaint')
    date = models.DateField()
    title = models.CharField(max_length=50)
    complaint =  models.TextField()
    
    def __str__(self):
        return self.title