from rest_framework import serializers
from .models import Post, Like
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    reply_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source="parent",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "type",
            "media_url",
            "created_at",
            "updated_at",
            "parent",
            "parent_id",
            "reply_count",
            "likes_count",
            "comment_count",
            "shares_count",
            "is_liked",
        ]
        read_only_fields = [
            "author",
            "created_at",
            "updated_at",
            "parent",
            "reply_count",
            "is_liked",
        ]

    def get_reply_count(self, obj):
        return obj.replies.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False


