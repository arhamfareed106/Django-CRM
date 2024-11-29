import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcrm.settings')
django.setup()

from website.models import Record

def create_sample_data():
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
    for _ in range(100):
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

if __name__ == '__main__':
    print("Generating 100 sample records...")
    create_sample_data()
    print("Sample data generation complete!")
