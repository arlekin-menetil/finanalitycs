from django.db import models

class PhoneAuth(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone