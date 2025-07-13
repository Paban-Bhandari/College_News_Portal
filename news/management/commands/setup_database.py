from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Set up database for production deployment'

    def handle(self, *args, **options):
        self.stdout.write('Setting up database...')
        
        # Check if we're in production (DATABASE_URL is set)
        if os.environ.get('DATABASE_URL'):
            self.stdout.write('Production environment detected - using PostgreSQL')
        else:
            self.stdout.write('Development environment detected - using SQLite')
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('migrate')
        
        # Create superuser if it doesn't exist
        try:
            from django.contrib.auth.models import User
            if not User.objects.filter(is_superuser=True).exists():
                self.stdout.write('Creating superuser...')
                call_command('createsuperuser', interactive=False)
                self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            else:
                self.stdout.write('Superuser already exists')
        except Exception as e:
            self.stdout.write(f'Error creating superuser: {e}')
        
        # Populate sample data if needed
        try:
            from news.models import Article
            if not Article.objects.exists():
                self.stdout.write('Populating sample data...')
                call_command('populate_sample_data')
                self.stdout.write(self.style.SUCCESS('Sample data populated successfully'))
            else:
                self.stdout.write('Sample data already exists')
        except Exception as e:
            self.stdout.write(f'Error populating sample data: {e}')
        
        self.stdout.write(self.style.SUCCESS('Database setup completed successfully')) 