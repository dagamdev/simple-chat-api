from rest_framework.serializers import ModelSerializer
from .models import CustomUser, Conversation, Message

class UserSerializer(ModelSerializer):
  class Meta:
    model = CustomUser
    exclude = ['password', 'last_login']

class ConversationSerializer(ModelSerializer):
  class Meta:
    model = Conversation
    fields = '__all__'

class MessageSerializer(ModelSerializer): 
  class Meta:
    model = Message
    fields = '__all__'