from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website.models import Record
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate 100 sample records'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Create a test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()

        # Generate 100 fake records
        for i in range(100):
            Record.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                zipcode=fake.zipcode(),
                created_by=user
            )
            if (i + 1) % 10 == 0:
                self.stdout.write(self.style.SUCCESS(f'Created {i + 1} records...'))
        
        self.stdout.write(self.style.SUCCESS('Successfully generated 100 sample records'))
