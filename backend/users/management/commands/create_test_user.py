# � NATALIA - Auth & Users Lead
# create_test_user.py - Management command for dev setup
# Run with: python manage.py create_test_user
"""
TODO: Create management command to generate test user

This command creates a test user for development/demo purposes.
Run it with: python manage.py create_test_user

What it should do:
1. Define test credentials (username, email, password)
2. Check if user already exists (User.objects.filter(username=...).exists())
3. If not exists, create User with create_user() (auto-hashes password!)
4. Create or update associated Profile
5. Print success messages using self.stdout.write()

This is useful for:
- Quick setup after fresh database
- Demo purposes
- Testing without manual signup

Think about:
- What if user already exists? (Check first, skip or update)
- Should password be hardcoded or accept as argument?
- What default profile data to set?

Hint: Inherit from BaseCommand
Hint: Use User.objects.create_user() for proper password hashing
Hint: Use Profile.objects.get_or_create() for profile
Hint: self.stdout.write(self.style.SUCCESS('message')) for success output
Hint: self.stdout.write(self.style.WARNING('message')) for warning output
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile


class Command(BaseCommand):
    help = 'Creates a test user for development'

    def handle(self, *args, **options):
        # Your code here
        pass

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('TEST USER READY!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Password: {password}')
        self.stdout.write('')
        self.stdout.write('Login at: POST /api/auth/login/')
        self.stdout.write('Body: {"username": "pabloPistola", "password": "test123"}')
        self.stdout.write('')
