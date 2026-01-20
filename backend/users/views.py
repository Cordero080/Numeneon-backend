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
from .serializers import EmailLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class ProfileViewSet(viewsets.ModelViewSet):
    """
    TODO: ViewSet for Profile CRUD operations
    
    - queryset: All Profile objects
    - serializer_class: ProfileSerializer
    - Override perform_create to auto-assign logged-in user
    
    Hint: serializer.save(user=self.request.user)
    """
    # handles CRUD for Profile model. Only users can create/edit their own profiles.
    queryset = Profile.objects.all() # grab all profiles
    serializer_class = ProfileSerializer # use ProfileSerializer for serialization
    permission_classes = [IsAuthenticated] # Only logged-in users can access

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign logged-in user as profile owner


@api_view(['POST']) 
@permission_classes([AllowAny]) # Allow anyone to access signup
# this is a POST view where we manually create User and their associated Profile
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
    # destructure request data
    data = request.data
    username = data.get('username')
    display_name = data.get('display_name', '')
    email = data.get('email')
    password = data.get('password')
    # validate required fields
    if not all([username, email, password]):
        return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
    # parse display_name
    name_parts = display_name.split(' ', 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    # create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    # create profile
    profile = Profile.objects.create(user=user)
    # return success response
    return Response({'message': 'User created successfully.', 'user': {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile': ProfileSerializer(profile).data
    }}, status=status.HTTP_201_CREATED)


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
    serializer = EmailLoginSerializer(data=request.data)
    if serializer.is_valid():
        # the serializers handles the authentications and token generation
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    else: # if credentials are invalid
        error_msg = serializer.errors.get('non_field_errors', ['Invalid credentials.'])[0]
        return Response({'error': error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    # skipping usernames and using email. This uses a custom serializer to handle that, imported in serializers.py


@api_view(['GET'])
@permission_classes([IsAuthenticated]) # only logged-in users can access
# this is  the 'who am I' endpoint returning current user info. The frontend hits this on refresh to see if the stored token is still valid.
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
    user = request.user # populated by JWT middleware
    try:
        # fetch the profile, use sterializer to get the nested data
        profile_data = ProfileSerializer(user.profile).data
    except Profile.DoesNotExist:
        profile_data = None
    # return user data with nested profile
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'profile': profile_data
    })