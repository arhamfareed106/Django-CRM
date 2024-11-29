from django.core.management.base import BaseCommand
from website.models import Record
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random
from faker import Faker
import pytz

class Command(BaseCommand):
    help = 'Generates random records for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of records to generate')

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']
        
        # Ensure we have at least one user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )
        if created:
            user.set_password('admin123')
            user.save()

        # US States and their abbreviations
        states = {
            'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
            'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
            'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
            'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
            'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
            'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
            'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
            'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
            'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
            'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
        }

        # Generate records with varying creation dates
        end_date = datetime.now(pytz.UTC)
        start_date = end_date - timedelta(days=90)  # Generate data for the last 90 days

        self.stdout.write(self.style.SUCCESS(f'Generating {count} records...'))

        records = []
        for _ in range(count):
            # Generate a random date between start_date and end_date
            created_at = start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )

            # Select a random state
            state_name = random.choice(list(states.keys()))
            state_code = states[state_name]

            # Generate phone number in format (XXX) XXX-XXXX
            phone = f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"

            # Create record
            record = Record(
                created_at=created_at,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=phone,
                address=fake.street_address(),
                city=fake.city(),
                state=state_code,
                zipcode=fake.zipcode(),
                created_by=user
            )
            records.append(record)

            # Batch create every 1000 records
            if len(records) >= 1000:
                Record.objects.bulk_create(records)
                records = []
                self.stdout.write(self.style.SUCCESS(f'Created 1000 records...'))

        # Create any remaining records
        if records:
            Record.objects.bulk_create(records)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} records'))
