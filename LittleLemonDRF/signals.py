from django.db.models.signals import post_migrate
from djoser.signals import user_registered
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='customer')
    Group.objects.get_or_create(name='delivery_crew')
    Group.objects.get_or_create(name='manager')

@receiver(user_registered)
def add_user_to_customer_group(sender, user, request, **kwargs):
    customer_group = Group.objects.get(name="customer")
    customer_group.user_set.add(user)