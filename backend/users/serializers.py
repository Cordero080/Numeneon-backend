# 🟡 NATALIA - Auth & Users Lead
# serializers.py - Data conversion between Django models and JSON
"""
TODO: Create User Serializers - validate and format user data

Serializers do two jobs:
1. Validate incoming data (login form)
2. Format outgoing data (user JSON for frontend)

Serializers you need:
- EmailLoginSerializer: Custom login that accepts email + password, returns JWT tokens
- UserSerializer: Formats basic user data (id, username, email, first_name, last_name, date_joined)
- ProfileSerializer: Formats Profile data with nested user

IMPORTANT: Login uses EMAIL, not username!
EmailLoginSerializer:
- Fields: email, password (password is write_only)
- Validation: Look up user by email, authenticate with username
- Return: { access, refresh } JWT tokens

For UserSerializer:
- Include: id, username, email, first_name, last_name, date_joined
- Read-only: Don't allow editing user via this serializer

For ProfileSerializer:
- Include: id, user (nested UserSerializer), bio, avatar, location, website, created_at, updated_at
- user is read_only=True (nested)
- created_at, updated_at are read_only

Expected output format for profile:
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "date_joined": "2024-12-01T..."
  },
  "bio": "Hello world!",
  "avatar": "url or null",
  "location": "",
  "website": "",
  "created_at": "...",
  "updated_at": "..."
}

Think about:
- How do you look up user by email in validate()? (User.objects.get(email=email))
- How do you authenticate after finding user? (authenticate(username=user.username, password=password))
- How do you generate JWT tokens? (RefreshToken.for_user(user))
- Should password be write_only? (YES - never return passwords!)
- How do you nest UserSerializer inside ProfileSerializer? (user = UserSerializer(read_only=True))

Hint: Use serializers.Serializer for EmailLoginSerializer (custom validation)
Hint: Use serializers.ModelSerializer for ProfileSerializer and UserSerializer
Hint: For nested: user = UserSerializer(read_only=True)
Hint: For write_only: password = serializers.CharField(write_only=True)
Hint: Import: from rest_framework_simplejwt.tokens import RefreshToken
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile


class EmailLoginSerializer(serializers.Serializer):
    """
    TODO: Custom login serializer that accepts email + password
    Returns JWT access and refresh tokens.
    
    Fields:
    - email: EmailField
    - password: CharField (write_only=True!)
    
    In validate(self, data):
    1. Get email and password from data
    2. Look up user by email (User.objects.get(email=email))
    3. Authenticate with username (Django auth uses username internally)
    4. If authentication fails, raise ValidationError
    5. Check user.is_active
    6. Generate tokens: refresh = RefreshToken.for_user(user)
    7. Return { 'access': str(refresh.access_token), 'refresh': str(refresh) }
    
    Hint: authenticate(username=user.username, password=password)
    """
    # Your code here
    pass


class UserSerializer(serializers.ModelSerializer):
    """
    TODO: Basic user data serializer
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
    """
    # Your code here
    pass


class ProfileSerializer(serializers.ModelSerializer):
    """
    TODO: Profile serializer with nested user
    
    - user = UserSerializer(read_only=True)  # Nested, not editable
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar', 'location', 'website', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    """
    # Your code here
    pass