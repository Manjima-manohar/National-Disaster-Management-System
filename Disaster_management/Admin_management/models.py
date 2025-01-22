from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Government(models.Model):
    state_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='government_profile')
    
    def __str__(self):
        return self.state_name