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

  def retrieve(self, request: Request):
    user = request.user
    conversations = Conversation.objects.filter(participants=user)
    serializer = ConversationSerializer(conversations, many=True)

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

from .serializer import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def ping(request: Request):
  return Response({'message': 'Pong 🏓'})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def messages(request: Request):
  return Response({'message': f'messages by {request.user.name}'})

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
  print(request.user.email)
  user = get_object_or_404(CustomUser, email=request.user.email)

  if not user:
    return Response({'message': 'invalid token'})

  old_token = get_object_or_404(Token, user=user)
  old_token.delete()
  new_token = Token.objects.create(user=user)
  return Response({'token': new_token.key}, status=status.HTTP_200_OK)
  