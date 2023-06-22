from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create groups
        costumer_group, created = Group.objects.get_or_create(name='Customer')
        delivery_crew_group, created = Group.objects.get_or_create(name='delivery crew')
        manager_group, created = Group.objects.get_or_create(name='Manager')