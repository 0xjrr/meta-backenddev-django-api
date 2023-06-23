from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create groups
        costumer_group, created = Group.objects.get_or_create(name='customer')
        delivery_crew_group, created = Group.objects.get_or_create(name='delivery_crew')
        manager_group, created = Group.objects.get_or_create(name='manager')