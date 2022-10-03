from xml.dom import registerDOMImplementation
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Cart

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)