from email.policy import default
from itertools import product
from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name           = models.CharField(max_length=50, blank=True, null=True)
    description    = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name) 
    
    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')


class Product(models.Model):
    name            = models.CharField(max_length=50, blank=True, null=True)
    description     = models.CharField(max_length=255, blank=True, null=True)
    price           = models.PositiveIntegerField(default=0)
    under_category  = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return str(self.name) 
    
    class Meta:
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

    

class Cart(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username) 
    
    class Meta:
        verbose_name_plural = ('Carts')




class CartItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    count           = models.PositiveIntegerField(default=1)
    total_price     = models.PositiveIntegerField(default=0)
    cart            = models.ForeignKey('Cart', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.product.name) 
    
    class Meta:
        verbose_name_plural = ('Cart Items')