# 🟡 NATALIA - Auth & Users Lead
# views.py - Authentication and user management endpoints
"""
TODO: Create Authentication Views - signup, login, and current user endpoints

This file handles user registration, login, and fetching current user data.
Unlike Posts/Friends which use ViewSets, auth typically uses function-based views
or simple APIViews because the operations are unique (not standard CRUD).

Also includes a ProfileViewSet for profile CRUD operations.

Endpoints to create:
- POST /api/auth/signup/ - Create new user account
- POST /api/auth/login/ - Authenticate with EMAIL and return JWT tokens
- GET /api/auth/me/ - Get current logged-in user's data

IMPORTANT: Login uses EMAIL, not username!
Frontend sends: { "email": "user@example.com", "password": "..." }

For signup:
- Receive: { username, display_name, email, password }
- Parse display_name into first_name and last_name (split on first space)
- Validate: Username/email not taken
- Create: User + Profile
- Return: { id, username, email, message }

For login (email_login):
- Receive: { email, password }
- Look up user by email, then authenticate with username
- Return: JWT tokens { access, refresh }

For me (current_user):
- Require: Valid JWT token in Authorization header
- Return: Current user's data with nested profile

Expected response format for /api/auth/me/:
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "profile": {
    "id": 1,
    "bio": "Hello world!",
    "avatar": "url or null",
    "location": "",
    "website": ""
  }
}

Think about:
- How do you hash passwords? (Django's User.objects.create_user() handles this)
- Where do JWT tokens come from? (rest_framework_simplejwt is configured in settings)
- How do you return tokens on login? (RefreshToken.for_user(user))
- For /me/, how do you get the current user? (request.user when authenticated)
- What errors should you return? (400 for validation, 401 for bad credentials)
- How do you look up user by email? (User.objects.get(email=email))

Hint: Use @api_view(['POST']) decorator for function-based views
Hint: For JWT: from rest_framework_simplejwt.tokens import RefreshToken
Hint: Token generation: refresh = RefreshToken.for_user(user)
Hint: Use IsAuthenticated permission for /me/ endpoint
Hint: Use AllowAny for signup and login endpoints
Hint: Parse display_name: name_parts = display_name.split(' ', 1)
"""

from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    TODO: ViewSet for Profile CRUD operations
    
    - queryset: All Profile objects
    - serializer_class: ProfileSerializer
    - Override perform_create to auto-assign logged-in user
    
    Hint: serializer.save(user=self.request.user)
    """
    # Your code here
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    TODO: Create new user account
    
    Steps:
    1. Get username, display_name, email, password from request.data
    2. Parse display_name into first_name and last_name
    3. Validate required fields exist
    4. Check username not taken (User.objects.filter(username=username).exists())
    5. Check email not taken
    6. Create User with create_user() (auto-hashes password!)
    7. Create Profile for the user
    8. Return success response with user data
    
    Hint: User.objects.create_user(username=..., email=..., password=..., first_name=..., last_name=...)
    Hint: Profile.objects.create(user=user)
    """
    # Your code here
    pass


@api_view(['POST'])
@permission_classes([AllowAny])
def email_login(request):
    """
    TODO: Login with email and password, returns JWT tokens
    
    Steps:
    1. Import EmailLoginSerializer from .serializers
    2. Pass request.data to serializer
    3. If valid, return serializer.validated_data (contains tokens)
    4. If invalid, extract error message and return 401
    
    Hint: Use EmailLoginSerializer - it does the heavy lifting
    Hint: serializer.errors has the validation errors
    """
    # Your code here
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    TODO: Return currently logged-in user's info
    
    Steps:
    1. Get user from request.user (JWT middleware sets this)
    2. Try to get user's profile (user.profile)
    3. Serialize profile if exists, else None
    4. Return user data with nested profile
    
    Hint: Profile might not exist - use try/except
    Hint: ProfileSerializer(profile).data for serialization
    """
    # Your code here
    pass