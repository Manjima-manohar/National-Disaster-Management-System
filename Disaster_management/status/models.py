from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Make_alert(models.Model):
    issue = models.CharField(max_length=30)
    message = models.CharField(max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='make_alert')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.issue



