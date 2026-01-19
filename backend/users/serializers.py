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

# Actuan-based Serializers (manual control)
# serializers.serializer taking input (Email) and returning output (tokens)
class EmailLoginSerializer(serializers.Serializer):
    # get emai and password fields
    # what is Serializer expects from frontend (React)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True) # True to avoid password is never sent back in a JSON response
    # look up user by email and authenticate = security check
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = User.objects.get(email=email) # fetch user by email first
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        # authenticate with username
        user = authenticate(username=user.username, password=password)
        # # authenticate() checks the hashed password in the DB against the raw input
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        # generate JWT tokens
        refresh = RefreshToken.for_user(user) # user is legit, give tokens
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

# Model-based Serializers (automatic control)
# using ModelSerializer because we are serializing Django models directly
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # specify fields to include in serialized output
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

# Profile Serializer with nested UserSerializer (russian doll approach)
class ProfileSerializer(serializers.ModelSerializer):
    # This is "Nesting". We tell Django: "When you show a Profile, 
    # use the UserSerializer logic to show the owner's details too."
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        # specify fields to include in serialized output
        fields = ['id', 'user', 'bio', 'avatar', 'location', 'website', 'created_at', 'updated_at']
        # specify fields that are read-only and user cannot modify
        read_only_fields = ['created_at', 'updated_at']