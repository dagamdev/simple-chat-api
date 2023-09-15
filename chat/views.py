from rest_framework.viewsets import ModelViewSet
from .serializer import UserSerializer, ConversationSerializer, MessageSerializer
from .models import CustomUser, Conversation, Message
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

# Create your views here.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserView(ModelViewSet):
  serializer_class = UserSerializer
  queryset = CustomUser.objects.all()

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ConversationView(ModelViewSet):
  serializer_class = ConversationSerializer
  queryset = Conversation.objects.all()

  def list(self, request: Request):
    user = request.user
    conversations = Conversation.objects.filter(participants=user)

    updated_conversations = []
    for conversation in conversations:
      participants = [participant for participant in conversation.participants.all() if participant != request.user]

      updated_conversations.append({
        'id': conversation.id,
        'participants': participants,
        'created_at': conversation.created_at,
        'updated_at': conversation.updated_at
      })

    serializer = ConversationSerializer(updated_conversations, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MessageView(ModelViewSet):
  serializer_class = MessageSerializer
  queryset = Message.objects.all()

  def retrieve(self, request: Request):
    user = request.user
    messages = Message.objects.filter(author=user)
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


#* Separate views 
from .serializer import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def ping(request):
  return Response({'message': 'Pong 🏓'})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def users_me(request: Request):
  user_serializer = UserSerializer(instance=request.user)
  return Response(user_serializer.data)

@api_view(['get'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def conversation_messages(request: Request, id: str):
  try:
    conversation = get_object_or_404(Conversation, id=id)
    messages = Message.objects.filter(conversation=conversation)
    serializer = MessageSerializer(messages, many=True)

    return Response(serializer.data)
  except:
    return Response({'message': 'Invalid UUID identifier'}, status=status.HTTP_404_NOT_FOUND)    

@api_view(['POST'])
def signup(request: Request):
  user_serializer = UserSerializer(data=request.data)
  email = request.data.get('email')
  password = request.data.get('password')

  if not user_serializer.is_valid():
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  user_serializer.save()
  user = CustomUser.objects.get(email=email)
  user.set_password(password)
  user.save()
  token = Token.objects.create(user=user)
  return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request: Request):  
  email = request.data.get('email')
  password = request.data.get('password')
  
  if not (email and password):
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
  user = get_object_or_404(CustomUser, email=email)
  if not user.check_password(password):
    return Response({'message': 'Invalid password'}, status=status.HTTP_404_NOT_FOUND)
  
  [token, _] = Token.objects.get_or_create(user=user)
  user_serializer = UserSerializer(instance=user)
  return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def refresh_token(request: Request):  
  user = get_object_or_404(CustomUser, email=request.user.email)

  if not user:
    return Response({'message': 'invalid token'})

  old_token = get_object_or_404(Token, user=user)
  old_token.delete()
  new_token = Token.objects.create(user=user)
  return Response({'token': new_token.key}, status=status.HTTP_200_OK)
  