"""
Seed messages management command.

Usage:
    python manage.py seed_messages          # Add sample messages
    python manage.py seed_messages --clear  # Clear existing messages first
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from messages_app.models import Message


class Command(BaseCommand):
    help = 'Seeds the database with sample messages between users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing messages before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted_count = Message.objects.all().delete()[0]
            self.stdout.write(
                self.style.WARNING(f'Cleared {deleted_count} existing messages')
            )
        
        # Skip seeding if messages already exist (unless --clear was used)
        if not options['clear'] and Message.objects.exists():
            self.stdout.write(
                self.style.SUCCESS('Messages already exist, skipping seed. Use --clear to reset.')
            )
            return

        # Define all conversations as list of tuples
        # (sender_username, receiver_username, content, is_read)
        # NOTE: Using actual usernames from database (team accounts + seed users)
        conversations = [
            # Conversation 1: arthurb ↔ pabloPistola
            ('arthurb', 'pabloPistola', 'Knock-knock', True),
            ('pabloPistola', 'arthurb', "nobody's home", False),
            ('arthurb', 'pabloPistola', 'Damn', True),
            ('arthurb', 'pabloPistola', 'You still there?', False),

            # Conversation 2: natalia ↔ pabloPistola (team account)
            ('natalia', 'pabloPistola', "I don't know how I feel about this", True),
            ('pabloPistola', 'natalia', "I don't feel anything", False),
            ('natalia', 'pabloPistola', 'Hello??', False),
            ('natalia', 'pabloPistola', 'Answer me!', False),

            # Conversation 3: colin ↔ pabloPistola (team account)
            ('colin', 'pabloPistola', 'What do you think?', True),
            ('pabloPistola', 'colin', "You don't wanna know", False),
            ('colin', 'pabloPistola', 'Bro?', True),

            # Conversation 4: crystal ↔ pabloPistola (team account)
            ('crystal', 'pabloPistola', "So, I think I have some typo's", False),
            ('pabloPistola', 'crystal', 'I have dyslexia', False),

            # Conversation 5: titod ↔ pabloPistola
            ('titod', 'pabloPistola', 'Yo!', True),
            ('pabloPistola', 'titod', "You're alive!", False),
            ('titod', 'pabloPistola', 'Miss you!', False),
        ]

        created_count = 0
        errors = []

        for sender_name, receiver_name, content, is_read in conversations:
            try:
                sender = User.objects.get(username=sender_name)
                receiver = User.objects.get(username=receiver_name)
                Message.objects.create(
                    sender=sender,
                    receiver=receiver,
                    content=content,
                    is_read=is_read
                )
                created_count += 1
                self.stdout.write(f'  ✓ {sender_name} → {receiver_name}: "{content[:30]}..."')
            except User.DoesNotExist as e:
                error_msg = f'User not found: {sender_name} or {receiver_name}'
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(f'  ✗ {error_msg}'))

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} messages'))
        
        if errors:
            self.stdout.write(self.style.ERROR(f'Errors: {len(errors)}'))
            self.stdout.write('')
            self.stdout.write('Required users: pabloPistola, arthurb, nataliap, colinw, crystalr, titod')
            self.stdout.write('Make sure these users exist before running this command.')
