# 🟢 COLIN - Posts Backend Lead
# models.py - Database structure for posts
"""
TODO: Create the Post model - core content type for NUMENEON

A post is the main content users create. NUMENEON has 3 post types:
- 'thoughts': Text-only posts (displayed in left column of Timeline River)
- 'media': Posts with images (displayed in center column)
- 'milestones': Achievement posts (displayed in right column)

Posts can also be replies to other posts, creating threaded conversations.

Fields you need:
- author: Who created it? (ForeignKey to User)
- type: What kind? (CharField with choices: 'thoughts', 'media', 'milestones')
- content: The text content (TextField, max 500 chars, can be blank for media-only)
- media_url: Optional URL to media (URLField, NOT ImageField!)
- parent: Reply to which post? (ForeignKey to self, null for top-level posts)
- created_at: When created? (DateTimeField, auto-set)
- updated_at: When updated? (DateTimeField, auto-set on save)
- likes_count: Number of likes (IntegerField, default=0)
- comment_count: Number of comments (IntegerField, default=0)
- shares_count: Number of shares (IntegerField, default=0)

IMPORTANT: Use media_url (URLField) NOT image (ImageField)!
- media_url stores a URL string pointing to the image
- This is simpler than handling file uploads

Integration points:
- PostsContext (Colin's frontend) fetches and manages these
- Pablo's TimelineRiverFeed displays posts grouped BY USER (not by date!)
- Pablo's ProfileCard.jsx uses engagement metrics for analytics

Expected JSON format (from serializer):
{
  "id": 1,
  "author": { "id": 5, "username": "alice", "first_name": "Alice", "last_name": "Smith" },
  "type": "thoughts",
  "content": "Hello NUMENEON!",
  "media_url": null,
  "parent": null,
  "parent_id": null,
  "created_at": "2024-12-19T10:30:00Z",
  "likes_count": 42,
  "comment_count": 7,
  "shares_count": 3,
  "is_liked": false
}

Think about:
- How do you restrict 'type' to only 3 values? (choices parameter)
- How do you make a post reply to another post? (ForeignKey to 'self')
- What happens when author is deleted? (CASCADE - delete their posts too)
- What happens when parent post is deleted? (CASCADE or SET_NULL?)
- Should content be required? (No - media posts might be image-only)
- How do you order posts? (Meta class with ordering = ['-created_at'])

Hint: POST_TYPES = [('thoughts', 'Thoughts'), ('media', 'Media'), ('milestones', 'Milestones')]
Hint: type = models.CharField(max_length=20, choices=POST_TYPES, default='thoughts')
Hint: media_url = models.URLField(blank=True, null=True)
Hint: parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
Hint: created_at = models.DateTimeField(auto_now_add=True)
Hint: likes_count = models.IntegerField(default=0)
"""

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # Your code here
    pass


"""
TODO: Create the Like model - tracks which users liked which posts

This enables the like/unlike toggle functionality.
Each user can only like a post once (enforced by unique_together).

Fields you need:
- user: Who liked it? (ForeignKey to User)
- post: Which post? (ForeignKey to Post)
- created_at: When did they like it? (DateTimeField, auto-set)

CRITICAL: Use unique_together = ('user', 'post') in Meta class
This prevents duplicate likes and allows toggle logic in views.

Hint: class Meta: unique_together = ('user', 'post')
Hint: related_name='likes' on both ForeignKeys for easy access
Hint: Add __str__ method: return f"{self.user.username} likes post {self.post.id}"
"""

class Like(models.Model):
    # Your code here
    pass
