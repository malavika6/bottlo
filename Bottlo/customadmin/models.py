from django.db import models
import random
import string

# Create your models here.


def generate_coupon_code():
    # Generate a random combination of letters and digits for the code
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choices(letters_and_digits, k=10))

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, default=generate_coupon_code)
    discount = models.PositiveIntegerField()
    min_amount = models.IntegerField()
    active = models.BooleanField()
    active_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    