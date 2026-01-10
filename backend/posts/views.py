# 🟢 COLIN - Posts Backend Lead
# views.py - API endpoints for posts (using ViewSet approach)
"""
TODO: Create Posts API Views - full CRUD for posts + like toggle + share

This ViewSet handles all post operations via REST API.
Use ModelViewSet for automatic CRUD operations.

Endpoints (automatic from ModelViewSet):
- GET /api/posts/ - List all posts
- POST /api/posts/ - Create new post
- GET /api/posts/:id/ - Get single post
- PUT /api/posts/:id/ - Full update
- PATCH /api/posts/:id/ - Partial update
- DELETE /api/posts/:id/ - Delete post

Custom endpoints needed (use @action decorator):
- GET /api/posts/:id/replies/ - Get all replies to a post
- POST /api/posts/:id/like/ - Toggle like on a post
- POST /api/posts/:id/share/ - Increment share count

Like endpoint behavior:
- If user hasn't liked → create Like, increment likes_count
- If user already liked → delete Like, decrement likes_count
- Return updated post with is_liked: true/false

Share endpoint behavior:
- Simply increment shares_count on the post
- Return updated post with new shares_count

Permissions:
- All endpoints: Authenticated only (IsAuthenticated)

For get_queryset:
- list action: return only top-level posts (parent__isnull=True)
- Support ?username= query param to filter by user
- Other actions: return all posts

For perform_create:
- Automatically set author to request.user

Think about:
- How do you auto-set author on create? (Override perform_create())
- For /replies/, how do you filter by parent? (@action decorator + queryset filter)
- For /like/, how do you check if Like already exists? (Like.objects.filter())
- How do you toggle? (If exists → delete, else → create)

Hint: Use ModelViewSet for automatic CRUD
Hint: Override perform_create(self, serializer): serializer.save(author=self.request.user)
Hint: Use @action(detail=True, methods=['get']) for /replies/
Hint: Use @action(detail=True, methods=['post']) for /like/ and /share/
Hint: Toggle like: existing = Like.objects.filter(user=user, post=post).first()
Hint: If existing: existing.delete() else: Like.objects.create(user=user, post=post)
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    TODO: Implement the ViewSet
    
    Attributes:
    - serializer_class = PostSerializer
    - permission_classes = [permissions.IsAuthenticated]
    
    Methods to implement:
    - get_queryset(): Filter for list vs detail actions
    - perform_create(): Auto-set author
    - replies(): @action for GET /posts/:id/replies/
    - like(): @action for POST /posts/:id/like/
    - share(): @action for POST /posts/:id/share/
    """
    # Your code here
    pass
