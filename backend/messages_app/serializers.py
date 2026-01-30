from notifications.utils import notify_new_message
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user info for message display"""
    class Meta:
        model = User
        fields = ['id', 'username']


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
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"MessageSerializer.create called with: {validated_data}")
        
        receiver_id = validated_data.pop('receiver_id')
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            logger.error(f"User with id {receiver_id} does not exist")
            raise
            
        validated_data['receiver'] = receiver
        validated_data['sender'] = self.context['request'].user
        
        logger.info(f"Creating message from {validated_data['sender']} to {receiver}")
        
        # Create the message
        message = super().create(validated_data)
        
        logger.info(f"Message created with id: {message.id}")

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


class ConversationSerializer(serializers.Serializer):
    """Serializer for conversation list (grouped by user)"""
    user = UserBasicSerializer()
    last_message = MessageSerializer()
    unread_count = serializers.IntegerField()
