from django.db import models
from store.models import product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class Cartitem(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product


