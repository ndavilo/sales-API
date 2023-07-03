from django.db import models
from allusers.models import User
from products.models import Product
import random
import string


def orderItem_random_id():
    while True:
        random_id = ''.join(random.choices(string.digits, k=16))
        if not OrderItem.objects.filter(id=random_id).exists():
            return random_id

def order_random_id():
    while True:
        random_id = ''.join(random.choices(string.digits, k=16))
        if not Order.objects.filter(id=random_id).exists():
            return random_id

class Order(models.Model):
    id = models.CharField(primary_key=True, default=order_random_id, max_length=16, editable=False)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    paymentMethod = models.CharField(max_length=200,null=True,blank=True)
    taxPrice = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    shippingPrice = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    totalPrice = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    isDeliver = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False,null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"{self.createdAt} - {self.id}"


class OrderItem(models.Model):
    id = models.CharField(primary_key=True, default=orderItem_random_id, max_length=16, editable=False)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order  = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    qty = models.IntegerField(null=True,blank=True,default=0)
    price = models.DecimalField(max_digits=12,decimal_places=2,null=True,blank=True)
    image = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return f"{self.name} - {self.id}"
