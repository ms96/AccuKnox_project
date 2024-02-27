from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *

def validate_unique_email(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Please enter a valid email address")

    if User.objects.filter(email__iexact=email).exists():
        raise ValidationError("This email address is already in use")
