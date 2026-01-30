# 🟢 COLIN - Posts Backend Lead
# views.py - API endpoints for posts (using ViewSet approach)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer
from friends.models import Friendship
from notifications.utils import notify_new_post


class PostViewSet(viewsets.ModelViewSet):
 
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.objects.all()

        if self.action == "list":
            qs = qs.filter(parent__isnull=True)

            username = self.request.query_params.get("username")
            if username:
                # Profile page: show user's own posts AND posts on their wall
                from django.db.models import Q
                qs = qs.filter(
                    Q(author__username=username, target_profile__isnull=True) |  # Their own posts (not wall posts)
                    Q(target_profile__username=username)  # Posts on their wall
                )
            else:
                # Main feed: exclude wall posts (only show regular posts)
                qs = qs.filter(target_profile__isnull=True)

        return qs

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        
        # Notify all friends about the new post
        try:
            friendships = Friendship.objects.filter(user=self.request.user)
            post_data = PostSerializer(post, context={'request': self.request}).data
            
            for friendship in friendships:
                notify_new_post(friendship.friend.id, post_data)
        except Exception as e:
            # Don't fail the post creation if notifications fail
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send post notifications: {e}")

    @action(detail=True, methods=["get"])
    def replies(self, request, pk=None):
        post = self.get_object()
        replies = Post.objects.filter(parent=post)
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        existing = Like.objects.filter(user=user, post=post).first()
        if existing:
            existing.delete()
            post.likes_count = max(0, post.likes_count - 1)
        else:
            Like.objects.create(user=user, post=post)
            post.likes_count += 1

        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def share(self, request, pk=None):
        post = self.get_object()
        post.shares_count += 1
        post.save()

        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

