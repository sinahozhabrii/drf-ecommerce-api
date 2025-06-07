from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Customer

@receiver(post_save,sender = get_user_model())
def create_customer_profile_for_new_users(instance,sender,created,**kwargs):
    if created:
        Customer.objects.create(user=instance)