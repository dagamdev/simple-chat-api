from rest_framework.viewsets import ModelViewSet
from .serializer import UserSerializer, ConversationSerializer, MessageSerializer
from .models import CustomUser, Conversation, Message
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

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

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MessageView(ModelViewSet):
  serializer_class = MessageSerializer
  queryset = Message.objects.all()


from rest_framework.request import Request
from rest_framework.response import Response

from .serializer import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


@api_view(['GET'])
def ping(request: Request):
  return Response({'message': 'Pong 🏓'})

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request: Request):
  user_serializer = UserSerializer(data=request.data)
  email = request.data.get('email')
  password = request.data.get('password')

  if user_serializer.is_valid():
    user_serializer.save()
    user = CustomUser.objects.get(email=email)
    user.set_password(password)
    user.save()
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_201_CREATED)

  return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request):  
  email = request.data.get('email')
  password = request.data.get('password')
  # print(req.data)
  
  if not (email and password):
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
  
  user = authenticate(request, email=email, password=password)

  if user:
    [token, _] = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def refresh_token(request: Request):  
  user = CustomUser.objects.get(email=request.data.get('email'))

  if user:
    old_token = Token.objects.get(user=user)
    old_token.delete()
    new_token = Token.objects.create(user=user)
    return Response({'token': new_token.key}, status=status.HTTP_200_OK)
  
  return Response({'message': 'hola'})
  