from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class UserSerializer(ModelSerializer):
  email = serializers.CharField(required=False)
  username = serializers.CharField(required=False)

  class Meta:
    model = CustomUser
    exclude = ['password', 'last_login', 'is_superuser']

class ConversationSerializer(ModelSerializer):
  # participants = UserSerializer(many=True, read_only=True)

  class Meta:
    model = Conversation
    fields = '__all__'

class MessageSerializer(ModelSerializer): 
  class Meta:
    model = Message
    fields = '__all__'