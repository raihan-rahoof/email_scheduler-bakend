from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class UserVerification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))

    def __str__(self):
        return f"{self.email} 's otp"

    def is_expired(self):
        return timezone.now() > self.expires_at