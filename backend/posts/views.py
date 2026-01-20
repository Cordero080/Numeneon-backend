# 🟢 COLIN - Posts Backend Lead
# views.py - API endpoints for posts (using ViewSet approach)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
 
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Post.objects.all()

        if self.action == "list":
            qs = qs.filter(parent__isnull=True)

            username = self.request.query_params.get("username")
            if username:
                qs = qs.filter(author__username=username)

        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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

