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

#===========================================
# add a "delete_test_user" command to easily clean up database after testing
#===========================================


class Command(BaseCommand):
    help = 'Creates a test user for development'

    def handle(self, *args, **options):
        # 1. define test credentials - hard code for dev-only script
        username = 'pabloPistola'
        email = 'pablo@example.com'
        password = 'test123'

        # 2. check if user already exists before creating
        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            user = User.objects.create_user( # 3. create_user() hashes password
                # and fills the last_login and date_joined fields that Postgres wants automatically
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'User "{username}" created successfully.'))
        else:
            # if created is False, the user already in db grab the existing user object to use in profile creation
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))

        # 4.  profile sync - create or get existing profile
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Profile created for user "{username}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Profile for user "{username}" already exists.'))
        
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
