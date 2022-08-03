from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    nickname = models.TextField(max_length=10)
    description = models.TextField(blank=True, default="안녕하세요.")
    image = models.ImageField(blank=True, upload_to="accounts/profile_img")
    
    def __str__(self):
        return self.nickname
    
