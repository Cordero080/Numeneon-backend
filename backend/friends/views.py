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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_list(request):
    """
    Returns all friends of the logged-in user
    """
    user = request.user

    frienships = Friendship.objects.filter(user=user)

    friends = []
    for fs in friendships:
        friend = fs.friend
        friends.append({
            'id': friend.id,
            'username': friend.username,
            'last_name': friend.last_name
        })

    return Response(friends, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_requests(request):
    """
    Returns all pending friend requests TO the logged-in user
    """
    user = request.user

    requests = FriendRequest.objects.filter(to_user=user)

    pending = []
    for fr in requests:
        pending.append({
            'id': fr.id,
            'from_user': {
                'id': fr.from_user.id,
                'username': fr.from_user.username,
                'first_name': fr.from_user.first_name,
                'last_name': fr.from_user.last_name
            },
            'created_at': fr.created_at.isoformat()
        })
    return Response(pending, status=status.HTTP_200_OK)





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
            return Response({'error':'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(
            from_user=from_user,
            to_user=to_user
        )

        return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
 


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
        return Response({'error': 'Not authorized', status=status.HTTP_403_FORBIDDEN})

    Friendship.object.create(user=user, friend=fr.from_user)
    Friendship.objects.create(user=fr.from_user, friend=user)

    fr.delete()

    return Response({
        'message': 'Friend request accepted',
        'friend': {
            'id': fr.from_user.id,
            'usename': fr.from_user.username,
            'first_name': fr.from_user.first_name,
            'last_name': fr.from_user.last_name
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_request(request, request_id):
    """
    Declines a pending friend request
    """
    user = request.user

    try:
        fr = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    if fr.to_user != user:
        return Response({'message': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    
    fr.delete()

    return Response({'message': 'Friend request declined'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_friend(request, user_id):
    """
    Removes a friend from your friend list
    """
    me = request.user

    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    Friendship.objects.filter(user=me, friend=target).delete()
    Friendship.objects.filter(user=target, friend=me).delete()

    return Response({'message': 'Friend removed'}, status=status.HTTP_200_OK)