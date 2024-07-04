from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserModel(models.Model):
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.fullname
