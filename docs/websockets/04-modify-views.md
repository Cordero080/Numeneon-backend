# Step 4: Modify Existing Views

> **Time:** ~15 minutes  
> **Files:**
>
> - `backend/friends/views.py`
> - `backend/messages_app/serializers.py`

---

## Overview

Now we need to emit WebSocket notifications when:

1. Someone sends a friend request → notify recipient
2. Someone accepts a friend request → notify original sender
3. Someone sends a message → notify recipient

---

## Step 4.1: Modify Friends Views

**File:** `backend/friends/views.py`

### 4.1.1: Add Import at Top

Add this import at the top of the file:

```python
from notifications.utils import notify_friend_request, notify_friend_accepted
```

Your imports section should look like:

```python
# 🟣 CRYSTAL - Friends System Lead
# views.py - API endpoints for friend operations
"""
Create Friends API Views - manage friendships and requests
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship
from notifications.utils import notify_friend_request, notify_friend_accepted  # <-- ADD THIS
```

---

### 4.1.2: Update send_request View

Find the `send_request` function and add the notification **after** creating the FriendRequest:

**Before:**

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request, user_id):
    """
    Sends a friend request to another user
    """
    from_user = request.user

    try:
        to_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if from_user == to_user:
        return Response({'error': 'You cannot friend yourself'}, status=status.HTTP_400_BAD_REQUEST)

    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    if Friendship.objects.filter(user=from_user, friend=to_user).exists():
        return Response({'error': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)

    FriendRequest.objects.create(
        from_user=from_user,
        to_user=to_user
    )

    return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
```

**After:**

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request, user_id):
    """
    Sends a friend request to another user
    """
    from_user = request.user

    try:
        to_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if from_user == to_user:
        return Response({'error': 'You cannot friend yourself'}, status=status.HTTP_400_BAD_REQUEST)

    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    if Friendship.objects.filter(user=from_user, friend=to_user).exists():
        return Response({'error': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the friend request
    friend_request = FriendRequest.objects.create(
        from_user=from_user,
        to_user=to_user
    )

    # ✨ Send real-time notification to recipient
    notify_friend_request(
        to_user_id=to_user.id,
        from_user=from_user,
        request_id=friend_request.id
    )

    return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
```

**Key changes:**

1. Store the created FriendRequest in a variable (`friend_request`)
2. Call `notify_friend_request()` with the recipient's ID

---

### 4.1.3: Update accept_request View

Find the `accept_request` function and add the notification:

**Before:**

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, request_id):
    """
    Accepts a pending friend request
    """
    user = request.user

    try:
        fr = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    if fr.to_user != user:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    Friendship.objects.create(user=user, friend=fr.from_user)
    Friendship.objects.create(user=fr.from_user, friend=user)

    fr.delete()

    return Response({
        'message': 'Friend request accepted',
        'friend': {
            'id': fr.from_user.id,
            'username': fr.from_user.username,
            'first_name': fr.from_user.first_name,
            'last_name': fr.from_user.last_name
        }
    }, status=status.HTTP_201_CREATED)
```

**After:**

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, request_id):
    """
    Accepts a pending friend request
    """
    user = request.user

    try:
        fr = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    if fr.to_user != user:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    # Store the original sender before deleting the request
    original_sender = fr.from_user

    Friendship.objects.create(user=user, friend=original_sender)
    Friendship.objects.create(user=original_sender, friend=user)

    fr.delete()

    # ✨ Send real-time notification to original sender
    notify_friend_accepted(
        to_user_id=original_sender.id,
        friend=user  # The person who accepted
    )

    return Response({
        'message': 'Friend request accepted',
        'friend': {
            'id': original_sender.id,
            'username': original_sender.username,
            'first_name': original_sender.first_name,
            'last_name': original_sender.last_name
        }
    }, status=status.HTTP_201_CREATED)
```

**Key changes:**

1. Store `original_sender` before deleting the request
2. Call `notify_friend_accepted()` to notify the original sender

---

## Step 4.2: Modify Messages Serializer

**File:** `backend/messages_app/serializers.py`

We'll add the notification in the serializer's `create` method since that's where messages are created.

### 4.2.1: Add Import

Add this import at the top:

```python
from notifications.utils import notify_new_message
```

### 4.2.2: Update MessageSerializer.create()

**Before:**

```python
class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserBasicSerializer(read_only=True)
    receiver = UserBasicSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

    def create(self, validated_data):
        receiver_id = validated_data.pop('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        validated_data['receiver'] = receiver
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
```

**After:**

```python
class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserBasicSerializer(read_only=True)
    receiver = UserBasicSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']

    def create(self, validated_data):
        receiver_id = validated_data.pop('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        validated_data['receiver'] = receiver
        validated_data['sender'] = self.context['request'].user

        # Create the message
        message = super().create(validated_data)

        # ✨ Send real-time notification to recipient
        notify_new_message(
            to_user_id=receiver.id,
            message_data={
                'id': message.id,
                'sender': {
                    'id': message.sender.id,
                    'username': message.sender.username
                },
                'content': message.content,
                'created_at': message.created_at.isoformat()
            }
        )

        return message
```

**Key changes:**

1. Store the created message in a variable
2. Call `notify_new_message()` with the message data
3. Return the message

---

## Complete Modified Files

### backend/friends/views.py (relevant parts)

```python
# At the top
from notifications.utils import notify_friend_request, notify_friend_accepted

# In send_request function (after FriendRequest.objects.create)
    friend_request = FriendRequest.objects.create(
        from_user=from_user,
        to_user=to_user
    )

    notify_friend_request(
        to_user_id=to_user.id,
        from_user=from_user,
        request_id=friend_request.id
    )

# In accept_request function (before fr.delete())
    original_sender = fr.from_user
    # ... friendship creation ...
    fr.delete()

    notify_friend_accepted(
        to_user_id=original_sender.id,
        friend=user
    )
```

### backend/messages_app/serializers.py (relevant parts)

```python
# At the top
from notifications.utils import notify_new_message

# In create method
    def create(self, validated_data):
        # ... existing code ...
        message = super().create(validated_data)

        notify_new_message(
            to_user_id=receiver.id,
            message_data={
                'id': message.id,
                'sender': {
                    'id': message.sender.id,
                    'username': message.sender.username
                },
                'content': message.content,
                'created_at': message.created_at.isoformat()
            }
        )

        return message
```

---

## ✅ Checklist

- [ ] Added `notify_friend_request, notify_friend_accepted` import to `friends/views.py`
- [ ] Updated `send_request` view to call `notify_friend_request()`
- [ ] Updated `accept_request` view to call `notify_friend_accepted()`
- [ ] Added `notify_new_message` import to `messages_app/serializers.py`
- [ ] Updated `MessageSerializer.create()` to call `notify_new_message()`

---

## 🧪 How to Test

After completing all steps, you can test by:

1. Start the server: `python manage.py runserver`
2. Open browser console and connect to WebSocket
3. Use another browser/incognito to send a friend request
4. Watch the WebSocket receive the notification!

Detailed testing instructions are in [07-frontend-integration.md](./07-frontend-integration.md).

---

**Next Step:** [05-asgi-config.md](./05-asgi-config.md)
