from django.db import models
from django.conf import settings
from django.core.validators import MaxLengthValidator

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(validators=[
        MaxLengthValidator(limit_value=280, message="Content must be a maximum of 280 characters.")
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.created_at}'
