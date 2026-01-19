# 🟢 COLIN - Posts Backend Lead
# models.py - Database structure for posts

from django.conf import settings
from django.db import models


class Post(models.Model):
    POST_TYPES = [
        ("thoughts", "Thoughts"),
        ("media", "Media"),
        ("milestones", "Milestones"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    type = models.CharField(max_length=20, choices=POST_TYPES, default="thoughts")

    # Allow blank so media-only posts are possible
    content = models.TextField(max_length=500, blank=True)

    # URL to an image/video hosted elsewhere (NOT an ImageField)
    media_url = models.URLField(blank=True, null=True)

    # Replies: null for top-level posts
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        preview = (self.content or "").strip()
        if len(preview) > 30:
            preview = preview[:27] + "..."
        return f"{self.author} • {self.type} • {preview or '—'}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self) -> str:
        return f"{self.user} likes post {self.post_id}"

