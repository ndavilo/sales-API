from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.hashers import make_password

def get_default_group():
    # Retrieve or create the default group
    group, _ = Group.objects.get_or_create(name='visitors')
    return group


    
# Create your models here.
class User(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    lga = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group, blank=True, default=get_default_group)
    REQUIRED_FIELDS = ['phone_number', 'email']
    

    def set_password(self, raw_password):
        # Use Django's password hashing to securely set the password
        self._password = make_password(raw_password)
        
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.email} {self.phone_number}"
    

