# 🟢 COLIN - Posts Backend Lead
# serializers.py - Data conversion between Django models and JSON
"""
TODO: Create Post Serializer - formats post data for API responses

The serializer transforms Post model instances to JSON and validates incoming data.

Key requirement: Nested author data
- Don't just return author: 5 (the ID)
- Return author: { id: 5, username: "alice", first_name: "Alice", last_name: "Smith" }
- Pablo's components expect this nested format!

For input (creating posts):
- Accept: type, content, media_url, parent_id (NOT parent!)
- Don't accept: author, created_at, engagement counts (these are auto-set)

For output (returning posts):
- Include: id, author (nested), type, content, media_url, parent, parent_id, created_at, updated_at
- Include: likes_count, comment_count, shares_count (REQUIRED for ProfileCard analytics!)
- Include: is_liked (Boolean - has current user liked this post?)
- Include: reply_count (count of posts where parent=this post)
- Author should include: id, username, first_name, last_name

Fields to add:
- author = UserSerializer(read_only=True)  # Nested, not just ID
- parent_id = PrimaryKeyRelatedField for accepting parent in POST requests
- is_liked = SerializerMethodField  # Check if current user liked
- reply_count = SerializerMethodField  # Count replies

Think about:
- How do you nest author data? (Import and use UserSerializer from users app)
- Should author be read-only? (Yes - set automatically, not by user)
- How do you accept parent_id but store as parent? (source='parent' on PrimaryKeyRelatedField)
- How do you get current user in serializer? (self.context['request'].user)
- How do you check if user liked post? (Like.objects.filter(user=user, post=obj).exists())

Hint: from users.serializers import UserSerializer
Hint: author = UserSerializer(read_only=True)
Hint: parent_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='parent', write_only=True, required=False, allow_null=True)
Hint: is_liked = serializers.SerializerMethodField()
Hint: reply_count = serializers.SerializerMethodField()
Hint: def get_is_liked(self, obj): check if current user liked this post
Hint: def get_reply_count(self, obj): return obj.replies.count()
"""

from rest_framework import serializers
from .models import Post, Like
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    TODO: Implement the serializer
    
    Add these fields:
    - author = UserSerializer(read_only=True)
    - reply_count = serializers.SerializerMethodField()
    - is_liked = serializers.SerializerMethodField()
    - parent_id = serializers.PrimaryKeyRelatedField(...)
    
    Implement these methods:
    - get_reply_count(self, obj)
    - get_is_liked(self, obj)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'type', 'media_url', 'created_at', 
                  'updated_at', 'parent', 'parent_id', 'reply_count', 
                  'likes_count', 'comment_count', 'shares_count', 'is_liked']
        read_only_fields = ['author', 'created_at', 'updated_at', 'parent', 'reply_count', 'is_liked']
    """
    # Your code here
    pass
