from django.db import models
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError


def validate_phone(value):
    pattern = r'^[6-9]\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid 10-digit phone number.")


def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid 6-digit PIN code.")


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=10,
        validators=[validate_phone]
    )
    pincode = models.CharField(
        max_length=6,
        validators=[validate_pincode]
    )

    def __str__(self):
        return self.user.username