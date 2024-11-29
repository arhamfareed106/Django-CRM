from django.core.management.base import BaseCommand
from website.models import Record
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generates 100 sample records for the CRM'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Ensure we have at least one user
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

        # List of US states
        states = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]

        # Generate 100 records
        for _ in range(100):
            # Generate a random date within the last year
            created_date = datetime.now() - timedelta(
                days=random.randint(0, 365)
            )

            Record.objects.create(
                created_by=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.street_address(),
                city=fake.city(),
                state=random.choice(states),
                zipcode=fake.zipcode(),
                created_at=created_date
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully generated 100 sample records')
        )
